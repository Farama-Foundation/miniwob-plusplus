---
hide-toc: true
firstpage:
lastpage:
---

# MiniWoB++

```{image} /_static/img/showcase.gif
:width: 100%
:align: center
```

The MiniWoB++ library contains a collection of over 100 **web interaction environments**,
along with JavaScript and Python interfaces for programmatically interacting with them.
The Python interface follows the [Gymnasium](https://gymnasium.farama.org/) API
and uses [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)
to perform actions on the web browser. 

MiniWoB++ is an extension of the
[OpenAI MiniWoB benchmark](http://proceedings.mlr.press/v70/shi17a/shi17a.pdf),
and was introduced in the paper
[Reinforcement Learning on Web Interfaces using Workflow-Guided
Exploration](https://arxiv.org/abs/1802.08802).
If you use MiniWoB++ in your research, please use the following citation:

```bibtex
@inproceedings{liu2018reinforcement,
 author = {Evan Zheran Liu and Kelvin Guu and Panupong Pasupat and Tianlin Shi and Percy Liang},
 title = {Reinforcement Learning on Web Interfaces using Workflow-Guided Exploration},
 booktitle = {International Conference on Learning Representations ({ICLR})},
 url = {https://arxiv.org/abs/1802.08802},
 year = {2018},
}
```

```{toctree}
:hidden:
:caption: Introduction

content/getting_started
content/basic_usage
content/observation_space
content/action_space
```

```{toctree}
:hidden:
:caption: Environments

content/viewing
environments/list
content/javascript_api
content/demonstrations
```

```{toctree}
:hidden:
:caption: Development

Github <https://github.com/Farama-Foundation/miniwob-plusplus>
Contribute to the Docs <https://github.com/Farama-Foundation/miniwob-plusplus/blob/master/docs/README.md>
```
