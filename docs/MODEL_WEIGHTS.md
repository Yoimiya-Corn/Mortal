# Mortal 模型文件说明 / Model Weights Documentation

[中文](#中文说明) | [English](#english-version)

## 中文说明

### 关于 Mortal 模型权重文件

Mortal 是一个用于日本麻将的开源 AI 项目,基于深度强化学习技术。虽然代码是完全开源的,但**模型权重文件(.pth文件)并未公开发布**。

### 官方声明

根据项目维护者 Equim-chan 的说明,**目前尚未公开发布任何官方训练的模型权重**。在 [GitHub Discussion #97](https://github.com/Equim-chan/Mortal/discussions/97) 中,维护者明确表示:

> "As of now, I have not released any weights trained by myself to the public yet."
> 
> "截至目前,我还没有向公众发布任何我自己训练的权重。"

### 如何获取模型文件

README 中提到的 "Okay cool now give me the weights!" 部分引用了一个 Gist 帖子:
https://gist.github.com/Equim-chan/cf3f01735d5d98f1e7be02e94b288c56

**注意**: 此 Gist 可能包含获取模型的相关信息或说明。

### 可用选项

如果您想使用 Mortal AI,有以下几种方式:

#### 1. 自行训练模型

按照项目文档中的说明训练您自己的模型:
- 查看 [构建文档](https://mortal.ekyu.moe/user/build.html)
- 准备训练数据集(需要大量麻将对局记录)
- 配置训练参数(参考 `mortal/config.example.toml`)
- 需要GPU进行训练

#### 2. 查看相关项目

一些相关的项目和分支可能有额外的资源:

- **shinkuan/Mortal_v4**: 这个分支定期发布 libriichi 库文件
  - GitHub: https://github.com/shinkuan/Mortal_v4
  - 发布页面: https://github.com/shinkuan/Mortal_v4/releases
  - **注意**: 这些发布只包含编译好的 libriichi 库文件(.so, .pyd, .dylib),不包含模型权重文件

- **在线服务**: Mortal 提供了在线服务接口,详见 [文档](https://mortal.ekyu.moe/online/index.html)

#### 3. 社区资源

- 查看 [GitHub Discussions](https://github.com/Equim-chan/Mortal/discussions)
- 查看 [GitHub Issues](https://github.com/Equim-chan/Mortal/issues)
- 关注项目更新以获取模型发布的最新消息

### 模型文件格式

如果您成功训练或获取了模型,文件格式应该是:
- **PyTorch 模型文件**: `.pth` 或 `.pt` 格式
- **配置文件**: `config.toml` (配置模型参数)
- **放置位置**: 在配置文件中指定 `state_file` 路径

配置文件示例 (from `mortal/config.example.toml`):
```toml
[control]
state_file = '/path/to/mortal.pth'
```

### Docker 使用说明

如果使用 Docker,需要准备模型文件并挂载到容器中:

```bash
# 假设您的模型文件在 /path/to/model/dir 目录下
sudo docker run -i --rm -v /path/to/model/dir:/mnt mortal 2 < log.json
```

详见 [Docker 快速入门文档](https://mortal.ekyu.moe/user/docker.html)

### 最新更新 (2026年1月)

截至 2026年1月:
- ✅ 源代码: 完全开源并持续更新
- ✅ libriichi 库: 可从 shinkuan/Mortal_v4 获取预编译版本
- ❌ 模型权重: 官方未公开发布
- ℹ️ 模型获取: 需要参考 Gist 帖子或自行训练

### 相关链接

- 官方仓库: https://github.com/Equim-chan/Mortal
- 官方文档: https://mortal.ekyu.moe/
- Mortal_v4 分支: https://github.com/shinkuan/Mortal_v4
- 模型说明 Gist: https://gist.github.com/Equim-chan/cf3f01735d5d98f1e7be02e94b288c56

---

## English Version

### About Mortal Model Weights

Mortal is an open-source AI for Japanese mahjong powered by deep reinforcement learning. While the code is fully open source, **the model weight files (.pth files) are not publicly released**.

### Official Statement

According to the project maintainer Equim-chan, **no official trained model weights have been publicly released**. In [GitHub Discussion #97](https://github.com/Equim-chan/Mortal/discussions/97), the maintainer explicitly stated:

> "As of now, I have not released any weights trained by myself to the public yet."

### How to Get Model Files

The "Okay cool now give me the weights!" section in the README references a Gist post:
https://gist.github.com/Equim-chan/cf3f01735d5d98f1e7be02e94b288c56

**Note**: This Gist may contain information or instructions about obtaining models.

### Available Options

If you want to use Mortal AI, here are your options:

#### 1. Train Your Own Model

Follow the project documentation to train your own model:
- See [Build Documentation](https://mortal.ekyu.moe/user/build.html)
- Prepare training dataset (requires many mahjong game records)
- Configure training parameters (refer to `mortal/config.example.toml`)
- GPU required for training

#### 2. Related Projects

Some related projects and forks may have additional resources:

- **shinkuan/Mortal_v4**: This fork regularly releases libriichi library files
  - GitHub: https://github.com/shinkuan/Mortal_v4
  - Releases: https://github.com/shinkuan/Mortal_v4/releases
  - **Note**: These releases only include compiled libriichi library files (.so, .pyd, .dylib), not model weights

- **Online Service**: Mortal provides online service APIs, see [documentation](https://mortal.ekyu.moe/online/index.html)

#### 3. Community Resources

- Check [GitHub Discussions](https://github.com/Equim-chan/Mortal/discussions)
- Check [GitHub Issues](https://github.com/Equim-chan/Mortal/issues)
- Follow project updates for news about model releases

### Model File Format

If you successfully train or obtain a model, the file format should be:
- **PyTorch model file**: `.pth` or `.pt` format
- **Configuration file**: `config.toml` (configures model parameters)
- **Placement**: Specify `state_file` path in configuration

Configuration example (from `mortal/config.example.toml`):
```toml
[control]
state_file = '/path/to/mortal.pth'
```

### Docker Usage

When using Docker, you need to prepare the model file and mount it into the container:

```bash
# Assuming your model file is in /path/to/model/dir
sudo docker run -i --rm -v /path/to/model/dir:/mnt mortal 2 < log.json
```

See [Docker Quick Start Documentation](https://mortal.ekyu.moe/user/docker.html)

### Latest Update (January 2026)

As of January 2026:
- ✅ Source Code: Fully open source and continuously updated
- ✅ libriichi Library: Pre-compiled versions available from shinkuan/Mortal_v4
- ❌ Model Weights: Not officially released
- ℹ️ Model Access: Refer to Gist post or train your own

### Related Links

- Official Repository: https://github.com/Equim-chan/Mortal
- Official Documentation: https://mortal.ekyu.moe/
- Mortal_v4 Fork: https://github.com/shinkuan/Mortal_v4
- Model Info Gist: https://gist.github.com/Equim-chan/cf3f01735d5d98f1e7be02e94b288c56
