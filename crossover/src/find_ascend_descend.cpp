/* this code will split file to ascend orbit and descend orbit.

    FILENAME.dat => FILENAME_A.dat, FILENAME_D.dat
*/
#include <vector>


// in polar region , no requirement to split ascend and descend, no maintain

struct point
{
    double lat;
    double lon;
    double height;
    double t;
};



/*
Split orbit points to ascend points and descend points.

direction indicate this ascend lat trend.
*/
void split_point(const vector<point> &orbit, vector<point> ascend, vector<point> descend, int direction){
    size_t n = orbit.size();
    for(size_t i; i<n; ++i){
        if(((orbit[i+1].lat - orbit[i].lat)> 0) == direction){ // or u can find the change point, then don't need to judge every time
            ascend.push_back(orbit[i]);
        } else {
            descend.push_back(orbit[i]);
        }
    }
}

void split_file(const string &filename, int direction) {
    vector<point> orbit, ascend, descend;
    read_file(filename, orbit);
    split_point(orbit, ascend, descend, direction);
    write_to_file(ascend, filename.replace(-4, 3, "_A.dat"));
    write_to_file(descend, filename.replace(-4, 3, "_D.dat"));
}