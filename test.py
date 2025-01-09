import tensorflow as tf
print(tf.__version__)
# 因为是版本冲突了，这里无法导入 import keras
import tensorflow.keras as tk
tk.__version