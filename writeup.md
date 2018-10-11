# Patch the XSS Game

This webapp is deployed to Google App Engine at https://patch-the-xss-game.appspot.com

For the code patching the xss vulnerabilities, I've add the `@xss` tag comments in the source code. As for our Content Security Policy code, you can also use `@csp` to look for additional protection that we've made.

## Patch the XSS

### Level 1

Disable `self.response.headers.add_header("X-XSS-Protection", "0")`, so that when malicious users trying to inject `<script>` tag, the browser will block them and prevent the Javascript code from executing.

### Level 2

```js
DB.save(message.replace(/</g, "&lt;").replace(/>/g, "&gt;"), function () { displayPosts() });
```

Replace the `<` and `>` characters in message input, so that the users cannot inject javascript using html tag like `<img src="nah" onerror="alert()">`

### Level 3

```js
chooseTab(unescape(parseInt(self.location.hash.substr(1))));
```

Using `parseInt` javascript function to prevent malicious users from modify the URL. If the user input `#4' onerror="alert()" alt='exploited_image`, the parsed result will become only `#4`, thus xss injection will not happen.

### Level 4

In this level, we patch the xss vulnerability in `webapp.py` request handler.

```python
int(self.request.get('timer', 0))
timer = str(int(self.request.get('timer', 0)))
self.render_template('timer.html', {'timer': timer})
```

The vulnerability comes from user can input any type of data. So to prevent it, we only accept Integer input, otherwise an error will be raised and display the error message in the html page.

### Level 5

In this case we figure out that either App Engine or modern browsers will automatically escape the javascript code from URL. So if we inject the URL `https://patch-the-xss-game.appspot.com/level-5/signup?next=javascript:alert()` and click signup button, the page will be redirected to `https://patch-the-xss-game.appspot.com/level-5/javascriptalert()`, which will result in *404 Not Found**.


### Level 6
```js
if (url.match(/^https?:\/\//) || !url.endsWith(".js")) {
    setInnerText(document.getElementById("log"),
        "Sorry, cannot load a URL containing \"http\".");
    return;
}
```

In this case, we block all the URLs with .js extension. So any external javascript cannot be loaded in this case.

## Content Security Policy

### Level 1

Add the Content Security Policy from the server's response header.

```python
self.response.headers.add_header(
    "Content-Security-Policy", "script-src 'self' style-src 'self'")
```

### Level 2
```html
<meta http-equiv="Content-Security-Policy" content="script-src 'self' 'nonce-987654321'">
```

### Level 3
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline'; script-src 'self' ajax.googleapis.com 'nonce-12345' 'unsafe-eval';">
```

### Level 4
```html
<meta http-equiv="Content-Security-Policy" content="script-src 'self' 'unsafe-eval' 'nonce-999' 'nonce-888'">
```

### Level 5
```html
<meta http-equiv="Content-Security-Policy" content="script-src 'self'">
```

### Level 6
```html
<meta http-equiv="Content-Security-Policy" content="script-src * 'unsafe-inline'; connect-src 'self'">
```
