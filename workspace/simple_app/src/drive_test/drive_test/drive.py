import rclpy 
from rclpy.node import Node 
from lgsvl_msgs.msg import VehicleControlData, SignalArray

class Drive(Node): 
    def __init__(self): 
        self.go = False
        super().__init__('drive') 
        self.publisher_ = self.create_publisher(VehicleControlData, '/lgsvl/vehicle_control_cmd', 10) 
        timer_period = 0.1  # seconds 
        self.timer = self.create_timer(timer_period, self.timer_callback) 
        self.i = 0 

        # Subscribe Signal Sensor
        self.subscription = self.create_subscription(
            SignalArray,
            '/lgsvl/signal',
            self.signal_callback,10)

    def timer_callback(self): 
        msg = VehicleControlData()
        if(self.go):
            msg.acceleration_pct = 0.3
            msg.braking_pct = 0.0
        else:
            msg.acceleration_pct = 0.0
            msg.braking_pct = 0.7
        self.publisher_.publish(msg) 
        self.get_logger().info('Publishing %d' % self.i) 
        self.i += 1 

    def signal_callback(self, msg):
        if(len(msg.signals) > 0):
            self.go = msg.signals[0].label == "green"

def main(args=None):
    rclpy.init(args=args) 
    drive = Drive() 
    rclpy.spin(drive) 
    # Destroy the node explicitly 
    # (optional - otherwise it will be done automatically 
    # when the garbage collector destroys the node object) 
    drive.destroy_node() 
    rclpy.shutdown()

if __name__ == '__main__':
    main()
