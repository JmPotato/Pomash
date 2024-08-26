# Pomash

**NOTICE: This repo is no longer maintained, please use [rsomhaP](https://github.com/JmPotato/rsomhaP) which is the latest refactored version.**

Pomash is a lightweight blog system. Powered by Tornado Web Framework. In an era that static blog generators and frontend-backend separated applications dominate, embrace this classic monolithic web application to embody a unique retro style.

## Deployment

Get Pomash:

```shell
git clone https://github.com/JmPotato/Pomash.git
cd Pomash
```

After customizing `config.toml`, run `deploy.sh [PORT]` to deploy the Pomash automatically.

```shell
chmod +x deploy.sh && ./deploy.sh 5299
```

## Usage

Pomash uses Markdown to write posts and pages. LaTeX is also supported.

Note: To avoid conflict between LaTeX and Markdown, Pomash removed the emphasis syntax `*word*` and `_word_` which you should use `<em>word</em>` as an alternative.

    # Hello World

    ```python
    print('Hello, World!')
    ```

    Hello, World!

    Inline LaTeX: $\int_a^b f(x)\mathrm{d}x$

    New line LaTeX: $$\sum_{i=0}^{n}i^2$$

    <em>This is a emphasis.</em>

    **This is a double emphasis.**

    ~~This is a strikethrough.~~

    * Hello
    * World

## Themes

Pomash's theme is called Potheme. Here is a Potheme list:

* [Potheme-Clean](https://github.com/JmPotato/Pomash/tree/master/Pomash/theme/clean)
* [Potheme-Maupassant](https://github.com/JmPotato/Potheme-Maupassant)
* [Potheme-Default](https://github.com/JmPotato/Potheme-Default)

## References

A [Chinese guide](https://ipotato.me/article/16) for setting up.(Maybe a little outdated)

## License

Please read the [MIT-LICENSE](./LICENSE)
