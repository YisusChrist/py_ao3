<p align="center">
    <a href="https://github.com/YisusChrist/py_ao3/issues">
        <img src="https://img.shields.io/github/issues/YisusChrist/py_ao3?color=171b20&label=Issues%20%20&logo=gnubash&labelColor=e05f65&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/py_ao3/forks">
        <img src="https://img.shields.io/github/forks/YisusChrist/py_ao3?color=171b20&label=Forks%20%20&logo=git&labelColor=f1cf8a&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/py_ao3/stargazers">
        <img src="https://img.shields.io/github/stars/YisusChrist/py_ao3?color=171b20&label=Stargazers&logo=octicon-star&labelColor=70a5eb">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/py_ao3/actions">
        <img alt="Tests Passing" src="https://github.com/YisusChrist/py_ao3/actions/workflows/github-code-scanning/codeql/badge.svg">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/py_ao3/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/YisusChrist/py_ao3?color=0088ff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://opensource.org/license/GPL-3.0/">
        <img alt="License" src="https://img.shields.io/github/license/YisusChrist/py_ao3?color=0088ff">
    </a>
</p>

<br>

<p align="center">
    <a href="https://github.com/YisusChrist/py_ao3/issues/new?assignees=YisusChrist&labels=bug&projects=&template=bug_report.yml">Report Bug</a>
    ·
    <a href="https://github.com/YisusChrist/py_ao3/issues/new?assignees=YisusChrist&labels=feature&projects=&template=feature_request.yml">Request Feature</a>
    ·
    <a href="https://github.com/YisusChrist/py_ao3/issues/new?assignees=YisusChrist&labels=question&projects=&template=question.yml">Ask Question</a>
    ·
    <a href="https://github.com/YisusChrist/py_ao3/security/policy#reporting-a-vulnerability">Report security bug</a>
</p>

<br>

![Alt](https://repobeats.axiom.co/api/embed/cd9239ab8f98edef7010a72b2a01492ea28060de.svg "Repobeats analytics image")

<br>

`py_ao3` is a Python script that allows you to backup your GitHub repositories in a simple and fast way.

<details>
<summary>Table of Contents</summary>

- [Requirements](#requirements)
- [Installation](#installation)
  - [From PyPI](#from-pypi)
  - [Manual installation](#manual-installation)
  - [Uninstall](#uninstall)
- [Usage](#usage)
  - [Example of execution](#example-of-execution)
- [Contributors](#contributors)
  - [How do I contribute to py_ao3?](#how-do-i-contribute-to-py_ao3)
- [License](#license)
- [Credits](#credits)

</details>

## Requirements

Here's a breakdown of the packages needed and their versions:

- [poetry](https://pypi.org/project/poetry) >= 1.7.1 (_only for manual installation_)
- [chardet](https://pypi.org/project/chardet) >= 5.2.0
- [matplotlib](https://pypi.org/project/matplotlib) >= 3.9.1
- [rich](https://pypi.org/project/rich) >= 13.7.1
- [textual](https://pypi.org/project/textual) >= 0.74.0

> [!NOTE]
> The software has been developed and tested using Python `3.12.1`. The minimum required version to run the software is Python 3.6. Although the software may work with previous versions, it is not guaranteed.

## Installation

### From PyPI

`py_ao3` can be installed easily as a PyPI package. Just run the following command:

```bash
pip3 install py_ao3
```

> [!IMPORTANT]
> For best practices and to avoid potential conflicts with your global Python environment, it is strongly recommended to install this program within a virtual environment. Avoid using the --user option for global installations. We highly recommend using [pipx](https://pypi.org/project/pipx) for a safe and isolated installation experience. Therefore, the appropriate command to install `py_ao3` would be:
>
> ```bash
> pipx install py_ao3
> ```

The program can now be ran from a terminal with the `py_ao3` command.

### Manual installation

If you prefer to install the program manually, follow these steps:

> [!WARNING]
> This will install the version from the latest commit, not the latest release.

1. Download the latest version of [py_ao3](https://github.com/YisusChrist/py_ao3) from this repository:

   ```bash
   git clone https://github.com/YisusChrist/py_ao3
   cd py_ao3
   ```

2. Install the package:

   ```bash
   poetry install
   ```

3. Run the program:

   ```bash
   poetry run py_ao3
   ```

### Uninstall

If you installed it from PyPI, you can use the following command:

```bash
pipx uninstall py_ao3
```

## Usage

To run the program, simply execute the following command:

```bash
py_ao3
```

In order to use the program, you must have a valid text file that contains the information of the stories you want to process. The file must be in the following format:

```md
_[TITLE]_

- [CHARACTERS] ([SERIES])

- by [[AUTHOR]]([AUTHOR_URL]) → [WORDS]

- [RATING][COMMENT]
```

As you may see, Markdown syntax is used to format the text file, so the program will read the file and process the information accordingly. You are free to pass any text file you want, as long as it follows the format above.

### Example of execution

https://github.com/user-attachments/assets/2ce55013-a285-40dc-9843-5e5fa9892439

## Contributors

<a href="https://github.com/YisusChrist/py_ao3/graphs/contributors"><img src="https://contrib.rocks/image?repo=YisusChrist/py_ao3" /></a>

### How do I contribute to py_ao3?

Before you participate in our delightful community, please read the [code of conduct](https://github.com/YisusChrist/.github/blob/main/CODE_OF_CONDUCT.md).

I'm far from being an expert and suspect there are many ways to improve – if you have ideas on how to make the configuration easier to maintain (and faster), don't hesitate to fork and send pull requests!

We also need people to test out pull requests. So take a look through [the open issues](https://github.com/YisusChrist/py_ao3/issues) and help where you can.

See [Contributing Guidelines](https://github.com/YisusChrist/.github/blob/main/CONTRIBUTING.md) for more details.

## License

`py_ao3` is released under the [GPL-3.0 License](https://opensource.org/license/GPL-3.0).

## Credits

> [!NOTE]
> Thanks to the [Textualize](https://github.com/Textualize) team for the [textual](https://github.com/Textualize/textual) TUI framework, which was a great inspiration for me to develop this project.
