#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <thread>
#include <chrono>
#include <mutex>
#include <iostream>


// class Logger {
// public:
//     enum LogLevel {
//         TRUACE,
//         DEBUG,
//         INFO,
//         WARN,
//         ERROR
//     };
//     Logger(std::string level, std::string time, std::string log);

// private:
//     std::string level_;
//     std::string time_;
//     std::string log_;
// };

class AsyncLog {
public:
    AsyncLog();
    ~AsyncLog();
    
    void append(std::string log);
    void start(){
        thread_ = std::thread(&AsyncLog::thread, this);
    }
    void stop(){
        run_ = false;
    }

private:
    std::string buffer_;
    std::string out_;
    std::thread thread_;
    std::mutex mtx_; 
    bool run_;
    void output();
    void movebuf();
    void thread();
};


AsyncLog::AsyncLog(){
    run_ = true;
    start();
}

AsyncLog::~AsyncLog(){
    run_ = false;
    thread_.join();
}

void AsyncLog::thread(){
    // ???
    // ??????
    while(run_){
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        if(buffer_.size() > 0){
            movebuf();
            output();
        }
    }
}

void AsyncLog::movebuf(){
    std::unique_lock<std::mutex> lck{mtx_};
    out_ = buffer_;
    buffer_ = ""; 
}

void AsyncLog::append(std::string log){
    std::unique_lock<std::mutex> lck{mtx_};
    // ????????
    if(buffer_.size()+log.size()>100){
        movebuf();
        output();
        buffer_ = log;
    }
    buffer_ += log;
}

void AsyncLog::output(){
    std::unique_lock<std::mutex> lck{mtx_};
    std::cout << out_.size() << ":\n" << out_;
}


AsyncLog& operator<<(AsyncLog &logger, const std::string log){
    logger.append(log);
    return logger;
}

AsyncLog& operator<<(AsyncLog &logger, int log){
    logger.append(std::to_string(log));
    return logger;
}

static AsyncLog LOGGER;
#define LOG (LOGGER << __FILE__ << ":" << __LINE__ << ":" << __func__ << ":")
#endif