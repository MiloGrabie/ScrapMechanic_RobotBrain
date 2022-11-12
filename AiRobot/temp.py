import matplotlib
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from numpy import array

my_chain = Chain(name='left_arm', links=[
    OriginLink(),
    URDFLink(
      name="shoulder",
      origin_translation=array([-10, 0, 5]),
      origin_orientation=array([0, 0, 0]),
      rotation=array([0, 0, 1]),
    ),
    URDFLink(
      name="elbow",
      origin_translation=array([25, 0, 0]),
      origin_orientation=array([0, 0, 0]),
      rotation=array([0, 1, 0]),
    ),
    URDFLink(
      name="wrist",
      origin_translation=array([22, 0, 0]),
      origin_orientation=array([0, 0, 0]),
      rotation=array([0, 1, 0]),
    )
])

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# fig, ax = plot_utils.init_3d_figure()
my_chain.plot(my_chain.inverse_kinematics(array([10, 2, 10])), ax)
# plt.xlim(-0.1, 0.1)
# plt.ylim(-0.1, 0.1)
plt.show()