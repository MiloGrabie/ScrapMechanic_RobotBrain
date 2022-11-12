import matplotlib
import numpy as np
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from numpy import array
import matplotlib.pyplot as plt

my_chain = Chain(name='left_arm', links=
    [
        URDFLink(
          name="shoulder",
          origin_translation=array([0, 0, 0]),
          origin_orientation=array([0, 0, 0]),
          rotation=array([0, 0, 1]),
        ),
        URDFLink(
          name="shoulder",
          origin_translation=array([2, 0, 10]),
          origin_orientation=array([0, 0, 0]),
          rotation=array([0, -1, 0]),
        ),
        URDFLink(
          name="wrist",
          origin_translation=array([5, 0, 0]),
          origin_orientation=array([0, 0, 0]),
          rotation=array([0, -1, 0]),
        ),
        URDFLink(
          name="wrist",
          origin_translation=array([5, 0, 0]),
          origin_orientation=array([0, 0, 0]),
          rotation=array([0, 0, 0]),
        ),
    ],
    active_links_mask=[True, True, True, False]
)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.set_aspect('auto')
# ax.set_box_aspect([1,1,1])
# fig, ax = plot_utils.init_3d_figure()
my_chain.plot(my_chain.inverse_kinematics(array([3, 3, 2])), ax)
# plt.xlim(-0.1, 0.1)
# plt.ylim(-0.1, 0.1)
plt.show()