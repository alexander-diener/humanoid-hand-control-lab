#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

class FingerControllerNode : public rclcpp::Node {
public:
  FingerControllerNode() : Node("finger_controller_node"), target_(0.0), theta_(0.0), omega_(0.0) {
    target_sub_ = create_subscription<std_msgs::msg::Float64>(
        "/finger/target", 10,
        [this](const std_msgs::msg::Float64::SharedPtr msg) { target_ = msg->data; });

    torque_pub_ = create_publisher<std_msgs::msg::Float64>("/finger/torque_cmd", 10);

    timer_ = create_wall_timer(std::chrono::milliseconds(10), [this]() { control_step(); });
  }

private:
  void control_step() {
    // Minimal proportional placeholder for portfolio illustration.
    const double kp = 3.5;
    const double torque = kp * (target_ - theta_) - 0.1 * omega_;
    auto msg = std_msgs::msg::Float64();
    msg.data = torque;
    torque_pub_->publish(msg);
  }

  rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr target_sub_;
  rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr torque_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  double target_;
  double theta_;
  double omega_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FingerControllerNode>());
  rclcpp::shutdown();
  return 0;
}

