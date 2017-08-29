#include <iostream>
#include <uhd/usrp/multi_usrp.hpp>
#include <uhd/utils/msg.hpp>

class UsrpTest {

public:
  void open() {

    std::string device_args(
        "type=b200, send_frame_size=4096, recv_frame_size=4096");
    // auto usrp = uhd::usrp::multi_usrp::make(device_args);

    uhd::msg::register_handler(&UsrpTest::MsgHandler);
  }
  static void MsgHandler(uhd::msg::type_t type, const std::string &msg) {}
};

int main() { 
  UsrpTest usrp;
  usrp.open();
  std::cout << "Successfully open usrp\n";
}
