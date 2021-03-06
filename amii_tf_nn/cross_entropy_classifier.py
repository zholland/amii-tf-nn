import tensorflow as tf
from .estimator import Estimator


class CrossEntropyClassifer(Estimator):
    def _create_surrogate_eval(self):
        with tf.name_scope('xentropy'):
            diff = tf.nn.softmax_cross_entropy_with_logits(
                labels=self.target_node,
                logits=self.model.pre_activation()
            )
            node = tf.reduce_mean(diff)
        return node, 'xentropy'

    def _create_evals(self):
        with tf.name_scope('accuracy'):
            with tf.name_scope('correct_prediction'):
                correct_prediction = tf.equal(
                    tf.argmax(self.model.post_activation(), 1),
                    tf.argmax(self.target_node, 1)
                )
            acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        with tf.name_scope('L2_distance'):
            distance = 1 / 2.0 * tf.reduce_mean(
                tf.square(self.model.post_activation() - self.target_node)
            )
        return {'accuracy': acc, 'L2_distance': distance}
