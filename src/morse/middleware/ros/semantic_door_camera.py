import logging; logger = logging.getLogger("morse." + __name__)
import json
import roslib; roslib.load_manifest('rospy'); roslib.load_manifest('std_msgs')
import rospy
from std_msgs.msg import String
from morse.middleware.ros import ROSPublisherTF
from morse.middleware.socket_datastream import MorseEncoder

class SemanticDoorCameraPublisher(ROSPublisherTF):
    """ Publish the data of the semantic camera as JSON in a ROS String message.
    And send TF transform between '/map' and ``object.name``.
    """
    ros_class = String

    def default(self, ci='unused'):
        string = String()
        string.data = json.dumps(self.data['visible_doors'], cls=MorseEncoder)
        self.publish(string)


class SemanticDoorCameraPublisherLisp(ROSPublisherTF):
    """ Publish the data of the semantic camera as a ROS String message,
    that contains a lisp-list (each field are separated by a space).

    This function was designed for the use with CRAM and the Adapto group.
    """
    ros_class = String

    def default(self, ci='unused'):
        string = String()
        string.data = "("
        for obj in self.data['visible_doors']:
            # if object has no description, set to '-'
            if obj['description'] == '':
                description = '-'
            else:
                description = obj['description']

            # Build string from name, description, location and orientation in the global world frame
            string.data += "(" + str(obj['name']) + " " + description + " " + \
                           str(obj['hinge']) + " " + \
                           str(obj['open']) + ")"

        string.data += ")"
        self.publish(string)