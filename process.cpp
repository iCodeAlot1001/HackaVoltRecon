#include <boost/process.hpp>
#include <boost/asio.hpp>
#include <iostream>
#include <string>
#include <format>

namespace bp = boost::process;
namespace asio = boost::asio;

extern "C" {
    asio::io_context ioctx;
    void exit_handler(const boost::system::error_code& err, int rc) {
        if (!err) {
            std::cout << "Shell command finished with exit code: " << rc << std::endl;
        } else {
            std::cerr << "Shell command error: " << err.message() << std::endl;
        }
    }
    void process_data_input(char* Url, int Port){
        bp::async_system(ioctx, exit_handler, "nmap -p {} {} -v", Url, Port); 
        std::cout << "SUCCESS CODE WORKS";
    }
    void syscall(){
        
    }
}
