# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Test configs for roll."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v1 as tf
from tensorflow.lite.testing.zip_test_utils import create_tensor_data
from tensorflow.lite.testing.zip_test_utils import make_zip_of_tests
from tensorflow.lite.testing.zip_test_utils import register_make_test_function


@register_make_test_function()
def make_roll_tests(options):
  """Make a set of tests to do roll."""

  test_parameters = [
      # Scalar axis.
      {
          "input_dtype": [tf.float32, tf.int32],
          "input_shape": [[2, 4, 5], [3, 8, 4]],
          "shift": [1, -3, 5],
          "axis": [0, 1, 2],
      },
      # 1-D axis.
      {
          "input_dtype": [tf.float32, tf.int32],
          "input_shape": [[2, 4, 5], [3, 8, 4]],
          "shift": [[1], [-3], [5]],
          "axis": [[0], [1], [2]],
      },
      # Multiple axis.
      {
          "input_dtype": [tf.float32, tf.int32],
          "input_shape": [[2, 4, 5], [3, 8, 4]],
          "shift": [[1, 3, 2], [3, -6, 5], [-5, 7, 8]],
          "axis": [[0, 1, 2]],
      },
      # Duplicate axis.
      {
          "input_dtype": [tf.float32],
          "input_shape": [[2, 4, 5], [3, 8, 4]],
          "shift": [[1, 3, -2]],
          "axis": [[0, 1, 1]],
      },
  ]

  def build_graph(parameters):
    input_value = tf.compat.v1.placeholder(
        dtype=parameters["input_dtype"],
        name="input",
        shape=parameters["input_shape"])
    outs = tf.roll(
        input_value, shift=parameters["shift"], axis=parameters["axis"])
    return [input_value], [outs]

  def build_inputs(parameters, sess, inputs, outputs):
    input_value = create_tensor_data(parameters["input_dtype"],
                                     parameters["input_shape"])
    return [input_value], sess.run(
        outputs, feed_dict=dict(zip(inputs, [input_value])))

  make_zip_of_tests(options, test_parameters, build_graph, build_inputs)