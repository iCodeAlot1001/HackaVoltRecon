#include <boost/process.hpp>
#include <boost/asio.hpp>
#include <iostream>
#include <fstream>
#include <string>

namespace bp = boost::process;
namespace ba = boost::asio;

extern "C" {
    ba::io_context ioctx;
    void showTools(){
        
    }

    void exit_handler(const boost::system::error_code& err, int rc) {
        if (!err)
            std::cout << "Shell command finished with exit code: " << rc << std::endl;
        else
            std::cerr << "Shell command error: " << err.message() << std::endl;
    }

    void process_data_input(char* Url, int Port) {
        if (Port < 0 || Port > 65535) {
            std::cerr << "Invalid port number.\n";
            return;
        }

        std::string portStr = std::to_string(Port);

        bp::async_system(
            ioctx,
            exit_handler,
            "nmap",
            "-p", portStr,
            Url,
            "-v"
        );

        std::cout << "SUCCESS CODE WORKS\n";
    }
}
