# Model Weights / 模型权重

## 获取模型权重文件 (Getting Model Weight Files)

Mortal 的代码是完全开源的,但**模型权重文件(.pth 文件)并未公开发布**。

The code of Mortal is fully open source, but **model weight files (.pth files) are not publicly released**.

## 官方声明 (Official Statement)

根据项目维护者的说明,目前尚未公开发布任何官方训练的模型权重。

According to the project maintainer, no official trained model weights have been publicly released yet.

相关讨论: [GitHub Discussion #97](https://github.com/Equim-chan/Mortal/discussions/97)

## 获取模型的方式 (Ways to Get Models)

### 1. 参考 Gist 帖子 (Refer to Gist Post)

README 中提到的获取权重信息:
https://gist.github.com/Equim-chan/cf3f01735d5d98f1e7be02e94b288c56

此 Gist 包含关于模型权重的详细说明。

This Gist contains detailed information about model weights.

### 2. 自行训练模型 (Train Your Own Model)

您可以按照文档说明训练自己的模型:

You can train your own model following the documentation:

- 查看 [构建文档](build.md) / See [Build Documentation](build.md)
- 准备训练数据集 / Prepare training dataset
- 配置训练参数 / Configure training parameters
- 需要 GPU 支持 / Requires GPU

### 3. 相关资源 (Related Resources)

#### libriichi 库文件 (libriichi Library Files)

虽然模型权重未公开,但您可以从以下项目获取预编译的 libriichi 库:

While model weights are not public, you can get pre-compiled libriichi library from:

- **shinkuan/Mortal_v4**: https://github.com/shinkuan/Mortal_v4/releases
  - 最新发布: libriichi_2025.05.13
  - Latest release: libriichi_2025.05.13
  - 支持平台: Linux, Windows, macOS
  - Supported platforms: Linux, Windows, macOS
  - 注意: 仅包含库文件,不包含模型权重
  - Note: Only contains library files, not model weights

#### 在线服务 (Online Service)

Mortal 提供在线服务 API,无需本地模型文件:

Mortal provides online service API without requiring local model files:

详见: [在线服务文档](../online/index.md) / See: [Online Service Documentation](../online/index.md)

## 模型文件配置 (Model File Configuration)

如果您获得或训练了模型,需要在配置文件中指定路径:

If you obtain or train a model, you need to specify the path in the configuration file:

```toml
[control]
state_file = '/path/to/mortal.pth'
```

配置文件示例: `mortal/config.example.toml`

Configuration example: `mortal/config.example.toml`

## Docker 使用 (Docker Usage)

使用 Docker 时需要挂载模型文件目录:

When using Docker, you need to mount the model file directory:

```bash
# 假设模型文件在 /path/to/model/dir
# Assuming model file is in /path/to/model/dir
sudo docker run -i --rm -v /path/to/model/dir:/mnt mortal 2 < log.json
```

详见: [Docker 快速入门](docker.md) / See: [Docker Quick Start](docker.md)

## 社区支持 (Community Support)

寻求帮助或了解更多信息:

For help or more information:

- GitHub Discussions: https://github.com/Equim-chan/Mortal/discussions
- GitHub Issues: https://github.com/Equim-chan/Mortal/issues

## 最新更新 (Latest Updates)

截至 2026年1月 / As of January 2026:

- ✅ 源代码: 开源并持续更新 / Source code: Open source and actively maintained
- ✅ libriichi 库: 可获取 / libriichi library: Available
- ❌ 模型权重: 未公开发布 / Model weights: Not publicly released
- ℹ️ 获取途径: 参考 Gist 或自行训练 / How to get: Refer to Gist or train your own

## 相关链接 (Related Links)

- 官方仓库 / Official Repository: https://github.com/Equim-chan/Mortal
- 模型说明 / Model Info: https://gist.github.com/Equim-chan/cf3f01735d5d98f1e7be02e94b288c56
- Mortal_v4 发布 / Mortal_v4 Releases: https://github.com/shinkuan/Mortal_v4/releases
