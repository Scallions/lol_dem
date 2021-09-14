#include <iostream>
#include <boost/filesystem.hpp>
#include <string>
#include <fstream>
#include <sstream>
#include <cmath>
#include <iomanip>
#include <atomic>
#include <thread>
#include <chrono>

#include "Logger.hpp"
#include "threadpool.h"
#include "progressbar.hpp"


using namespace std;
using namespace indicators;


// 定义数据结构
struct first
{
	int met_seconds;
	unsigned int subseconds;
	unsigned int transmit_time_seconds;
	unsigned int transmit_time_fraction;
	int laser_energy;
	int transmit_width;
	int sc_longitude;
	int sc_latitude;
	unsigned int sc_radius;
	unsigned int selenoid_radius;
};
struct spot
{
	int longitude;
	int latitude;
	int radius;
	unsigned int range;
	int pulse;
	unsigned int energy;
	unsigned int background;
	unsigned int threshold;
	unsigned int gain;
	unsigned int shot_flag;
};
struct last
{
	unsigned short int offnadir_angle;
	unsigned short int emission_angle;
	unsigned short int solar_incidence;
	unsigned short int solar_phase;
	unsigned  int earth_range;
	unsigned short int earth_pulse;
	unsigned short int earth_energy;
};
struct all
{
	struct first a;
	struct spot b[5];
	struct last c;
};
struct point
{
	double lon, lat;
};
struct area
{
	point p[2];
	string filename;
	int tag;
	int pnum;
};
struct real
{
	unsigned int t1, t2;
	double alt[5];
	point poin[5];
	int flag[5];

};
struct single_real
{
	point p;
	double alt;
	int num;
	unsigned int t1, t2;

};

void swap(real &e, all  d)      //将读取结果转换为BLH
{
	for (int i = 0; i<5; i++)
	{
		if (d.b[i].longitude>0)
		{
			e.poin[i].lon = (double)d.b[i].longitude / (double)1E7;
		}
		else
		{
			e.poin[i].lon = (double)d.b[i].longitude / (double)1E7 + 360;
		}

		e.poin[i].lat = (double)d.b[i].latitude / (double)1E7;
		// e.alt[i] = d.b[i].radius / (double)1E6 - d.a.selenoid_radius / (double)1E6; //double(1737.4);
		e.alt[i] = d.b[i].radius / (double)1E6 - double(1737.4);
		// if(e.alt[i] < -1000 && d.b[i].range != UINT32_MAX){
		// 	// cout<<d.b[i].radius<< " " << d.a.selenoid_radius << " " << d.b[i].range << " " << d.a.sc_radius<<endl;
		// 	// cout<<e.alt[i]<< " ";
		// 	e.alt[i] = (d.a.sc_radius - d.a.selenoid_radius) / (double)1E6 - d.b[i].range / (double)1E6;
		// 	// cout<<e.alt[i]<<endl;
		// }
		e.t1 = d.a.transmit_time_seconds;
		e.t2 = d.a.transmit_time_fraction;
		e.flag[i] = d.b[i].shot_flag;
	}
}

bool in_area(double lon, double lat, double lon_down, double lon_up, double lat_down, double lat_up)//判断点是否在目标区域内 
{
	if ((lon<lon_up) && (lon>lon_down))
	{
		if ((lat<lat_up) && (lat>lat_down))
			return true;
		else
			return false;

	}
	else
	{
		return false;
	}
}

int main(int argc, char** argv)
{

    if(argc!=2 && argc != 6)
    {
		cout << "Argc not right: " << argc << endl;
        cout << "Usage:" << endl;
        cout << "   ./read_data <dat_dir> [REGION]" << endl;
        return 1;
    }

    string dir = argv[1];
	


	// double lon_down = 48.285536, lon_up = 211.296789, lat_down = -90, lat_up = -89.322266;
	// shoemaker
	double lon_down = 36.285536, lon_up = 49.296789, lat_down = -86.9, lat_up = -85.1;
	if(argc == 6){
		lon_down = atof(argv[2]);
		lon_up = atof(argv[3]);
		lat_down = atof(argv[4]);
		lat_up = atof(argv[5]);
	}

    // boost::filesystem::path dir_path("/home/cyf/Code/Jupyter/lol/dat/out");
    // boost::filesystem::path old_cpath = boost::filesystem::current_path();
    boost::filesystem::path dir_path(dir);
    // dir_path = old_cpath / dir_path;
    if(!boost::filesystem::exists(dir_path))  //推断文件存在性
    {
        cout << "Directory doesn't exists: " << dir_path << endl;
        return 1;
    }
	string dirname = to_string(lon_down)+","+to_string(lon_up)+","+to_string(lat_down)+","+to_string(lat_up);
    if(!boost::filesystem::exists(dir_path / dirname))  //推断文件存在性
    {
        boost::filesystem::create_directory(dir_path / dirname);
    }
    // boost::filesystem::path list_path("list.txt");

	// print some info
    cout << "++++++++++++++++++++++++++++++" << endl;
    cout << "       Start read data        " << endl;
    cout << "++++++++++++++++++++++++++++++" << endl;
	cout << "\tRead dir: " << dir_path.string() << endl;
	cout << "\tRead area: " << lon_down << "," << lon_up << "," << lat_down << "," << lat_up << endl;

    boost::filesystem::recursive_directory_iterator itEnd;
	ThreadPool pool(48);



	long long fileCount = 0;
	atomic_llong count(0);
	vector<future<void>> result_fs;


    for(boost::filesystem::recursive_directory_iterator itor( dir_path ); itor != itEnd ;++itor)
    {
        // 遍历文件夹
        // LOG << itor->path().extension().string() << "\n";
		// cout << itor->path().extension() << endl;
        if(itor->path().extension() == ".DAT") // 找到 dat 数据文件
        {
			++fileCount;
			boost::filesystem::path data_path = itor->path();
			result_fs.emplace_back(pool.enqueue([&, data_path](){
				// LOG << "Reading: " << itor->path().string() << "\n";
				// cout << "Reading: " << itor->path().string() << endl;

				ifstream dat_stream(data_path.string().c_str(), ios::binary);
				vector<ofstream> out_streams(10);
				vector<boost::filesystem::path> out_paths(10);

				// read data
				all data_all;
				real data_real;
				vector<int> counts(5); 
				vector<vector<single_real>> reals(5, vector<single_real>());
				vector<int> midxs(5,0);
				while(dat_stream.read((char*)&data_all, sizeof(data_all)))
				{
					// 读取数据
					swap(data_real, data_all);
					for(int i=0;i<5;++i){
						// if(in_area(data_real.poin[i].lon, data_real.poin[i].lat, lon_down, lon_up, lat_down, lat_up))
						if(data_all.b[i].radius!=-1 && (data_real.alt[i] < 11) && (data_real.alt[i] > -10) && in_area(data_real.poin[i].lon, data_real.poin[i].lat, lon_down, lon_up, lat_down, lat_up))
						{
							reals[i].push_back({data_real.poin[i], data_real.alt[i], counts[i], data_real.t1, data_real.t2});
							if(reals[i][midxs[i]].p.lat > data_real.poin[i].lat){
								midxs[i] = counts[i];
							}
							++counts[i];
						}
					}
				}

				// open stream
				for(int i=0; i<5; ++i){
					int n = reals[i].size();
					if(n<100) continue;
					string afilename = data_path.stem().string() + "_" + to_string(i+1) + ".AR";
					string dfilename = data_path.stem().string() + "_" + to_string(i+1) + ".DR";
					boost::filesystem::path aout_path = dir_path / dirname / afilename;
					boost::filesystem::path dout_path = dir_path / dirname / dfilename;
					out_streams[i<<1].open(dout_path.string().c_str());
					out_streams[i<<1|1].open(aout_path.string().c_str());
					out_paths[i<<1] = dout_path;
					out_paths[i<<1|1] = aout_path;

				}

				// write data
				for(int i=0; i<5; ++i){
					int n = reals[i].size();
					if(n<100) continue;
					for(int j = 0;j<n;++j){
						if(j<=midxs[i]){
							out_streams[i<<1|1] << fixed << setprecision(7)  << reals[i][j].p.lon << " " << reals[i][j].p.lat << " " << reals[i][j].alt << " " << reals[i][j].t1 <<" " << reals[i][j].t2/153390080<< endl;						
						}else{
							out_streams[i<<1] << fixed << setprecision(7)  << reals[i][j].p.lon << " " << reals[i][j].p.lat << " " << reals[i][j].alt << " " << reals[i][j].t1 << " " <<reals[i][j].t2/153390080<< endl;						
						}
					}
				}

				// close stream
				for(int i=0; i<5; ++i){
					#ifdef DEBUG 
						if(counts[i] > 100)
							cout << "DEBUG: read: " << i << " " << counts[i] << " " << midxs[i] << endl;
					#endif
					int n = reals[i].size();
					if(n<100) continue;
					out_streams[i<<1].clear();
					out_streams[i<<1|1].clear();
					out_streams[i<<1].close();
					out_streams[i<<1|1].close();
					// quailty control remove some file
					if(counts[i] < 100){
						boost::filesystem::remove(out_paths[i<<1]);
						boost::filesystem::remove(out_paths[i<<1|1]);
					}
					if(midxs[i] <= 5){
						boost::filesystem::remove(out_paths[i<<1|1]);
					}
					if(midxs[i] >= counts[i] - 5){
						boost::filesystem::remove(out_paths[i<<1]);
					}
				}
				dat_stream.clear();
				dat_stream.close();
				++count;
				// cout << endl;
        	}));
		}
    }

	ProgressBar bar{
		option::BarWidth{100},
		option::Start{"["},
		option::Fill{"■"},
		option::Lead{"■"},
		option::Remainder{"-"},
		option::End{" ]"},
		option::ForegroundColor{Color::cyan},
		option::PostfixText{"Finding crossover..."},
		option::ShowElapsedTime{true},
		option::ShowRemainingTime{true},
		// option::MaxProgress{count_all},
		option::FontStyles{std::vector<FontStyle>{FontStyle::bold},
		}
	};
    
	// 启动输出显示
	// long long last = 0;
	// thread t([&](){
	// 	while(true){
	// 		if(count == fileCount) return;
	// 		if(count==last) continue;
	// 		cout << "Read: " << count << "/" << fileCount << endl;
	// 		last = count;
	// 		this_thread::sleep_for(chrono::milliseconds(500));
	// 	}
	// });
	int count_ct = 0;
	for(auto && result_f: result_fs){
		result_f.get();
		++count_ct;
		if(count_ct % (fileCount / 100) == 0){
			bar.set_progress(count_ct * 100 / fileCount);
		}
	}
	bar.mark_as_completed();

	return 0;
}
