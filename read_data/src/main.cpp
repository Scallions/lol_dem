#include <iostream>
#include <boost/filesystem.hpp>
#include <string>
#include <fstream>
#include <sstream>
#include <cmath>
#include <iomanip>

using namespace std;

// 定义数据结构
struct first
{
	int met_seconds;
	unsigned int subseconds;
	int transmit_time_seconds;
	int transmit_time_fraction;
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
	int t1, t2;
	double alt[5];
	point poin[5];
	int flag[5];

};
struct single_real
{
	point p;
	double alt;
	int num;
	int t1, t2;

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
		e.alt[i] = d.b[i].radius / (double)1E6 - d.a.selenoid_radius / (double)1E6; //double(1737.4);
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

    if(argc!=2)
    {
        cout << "Usage:" << endl;
        cout << "   ./read_data <dat_dir>" << endl;
        return 1;
    }

    string dir = argv[1];

    // wtf 照抄就完事了
	double lon_down, lon_up, lat_down, lat_up;
	double lon_down0, lon_up0, lat_down0, lat_up0;
	lon_down = 48.285536, lon_up = 211.296789, lat_down = -90, lat_up = -89.322266;

    // some margin
	// lon_down0 = lon_down - 0.2;
	// lon_up0 = lon_up + 0.2;
	// lat_down0 = lat_down - 0.2;
	// lat_up0 = lat_up + 0.2;

    // boost::filesystem::path dir_path("/home/cyf/Code/Jupyter/lol/dat/out");
    // boost::filesystem::path old_cpath = boost::filesystem::current_path();
    boost::filesystem::path dir_path(dir);
    // dir_path = old_cpath / dir_path;
    if(!boost::filesystem::exists(dir_path))  //推断文件存在性
    {
        cout << "Directory doesn't exists: " << dir_path << endl;
        return 1;
    }
    if(!boost::filesystem::exists(dir_path / "out"))  //推断文件存在性
    {
        boost::filesystem::create_directory(dir_path / "out");
    }
    // boost::filesystem::path list_path("list.txt");

    cout << "++++++++++++++++++++++++++++++" << endl;
    cout << "       Start read data        " << endl;
    cout << "++++++++++++++++++++++++++++++" << endl;

    boost::filesystem::recursive_directory_iterator itEnd;
    for(boost::filesystem::recursive_directory_iterator itor( dir_path ); itor != itEnd ;++itor)
    {
        // 遍历文件夹
        // cout << itor->path().extension() << endl;
        if(itor->path().extension() == ".dat") // 找到 dat 数据文件
        {
            all data_all;
            real data_real;
            cout << "Reading: " << itor->path() << endl;
            for(int i=0; i<5; i++)
            {
                ifstream dat_stream(itor->path().string().c_str(), ios::binary);    
                string filename = itor->path().stem().string() + "_" + to_string(i+1) + ".txt";
                boost::filesystem::path out_path = dir_path / "out" / filename;
                ofstream out_stream(out_path.string().c_str());
                bool flag = true; // 删除无数据文件
                int count = 0; // 统计点数
                while(dat_stream.read((char*)&data_all, sizeof(data_all)))
                {
                    // 读取数据
                    swap(data_real, data_all);
                    if(data_all.b[i].radius!=-1 && (data_real.alt[i] < 11) && (data_real.alt[i] > -10) && in_area(data_real.poin[i].lon, data_real.poin[i].lat, lon_down, lon_up, lat_down, lat_up))
                    {
                        flag = false;
                        count++;
                        // cout << "Find: " << itor->path() << endl;
                        // 如果有在范围内的点 追加到 txt 文件中
                        out_stream << fixed << setprecision(7)  << data_real.poin[i].lon << " " << data_real.poin[i].lat << " " << data_real.alt[i] << endl; //<< " " << data_real.t1 << " " << data_real.t2 << endl;
                        // break;
                    }
                }
                // break;
                if(flag)
                {
                    boost::filesystem::remove(out_path.string());
                }
                out_stream.clear();
                out_stream.close();
                dat_stream.clear();
                dat_stream.close();
                cout << i+1 << ": " << count << "   ";
            }
            cout << endl;
        }

    }
    return 0;
}
