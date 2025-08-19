## Learning FastAPI

Youtube sources : 
[Full basic](https://www.youtube.com/watch?v=iWS9ogMPOI0&t=66s)


## To add SSH key to github

- Open GitBash and execute following command - 
```ssh-keygen -t ed25519 -C "youremail@example.com"```

- Keep pressing enter till you get the key's randomart image in the terminal.

- Next execute the following command - 
```clip < ~/.ssh/id_ed25519.pub```

- This copies your SSH key in local system to clipboard. 

- Open Github, navigate to Settings > SSH and GPG keys > New SSH key.

- Paste the SSH key.

- To test if Github recognizes the key, execute - 
```ssh -T git@github.com```
