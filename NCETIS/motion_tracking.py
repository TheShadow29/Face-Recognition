#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#include <iostream>
#include <string>
#include <stdio.h>

using namespace std;
using namespace cv;

void detectAndDisplay( Mat frame );

String face_cascade_name = "haarcascade_frontalface_alt.xml";
CascadeClassifier face_cascade("/home/sravan/ImageProcessing/opencv/opencv-3.0.0-alpha/data/haarcascades/haarcascade_frontalface_alt.xml");

string window_name = "Capture - Face detection";

string person0 ="/home/sravan/ImageProcessing/NCETIS/person0/face";
string person1 ="/home/sravan/ImageProcessing/NCETIS/person1/face";
string person2 ="/home/sravan/ImageProcessing/NCETIS/person2/face";
string person3 ="/home/sravan/ImageProcessing/NCETIS/person3/face";
string person4 ="/home/sravan/ImageProcessing/NCETIS/person4/face";
bool firstTime= true;
int p0=0,p1=0,p2=0,p3=0,p4=0;
RNG rng(12345);

int main( int argc, const char** argv )
{
	VideoCapture capture(0);
	Mat frame;
	
	

	if( !face_cascade.load( face_cascade_name ) )
	{ 
		printf("--(!)Error loading\n"); 
		return -1; 
	}

	if( capture.isOpened() )
	{
		while( true )
		{
    			capture >>frame;
			
			if( !frame.empty() )
			{	 
				std::vector<Rect> faces;
				Mat frame_gray;
	
				cvtColor( frame, frame_gray, COLOR_BGR2GRAY );
				equalizeHist( frame_gray, frame_gray);
	
				face_cascade.detectMultiScale( frame_gray, faces, 1.1, 3, 0, Size(30, 30) );
				
				Point current_center[faces.size()];	
				Point previous_center[faces.size()];

				for( size_t i = 0; i < faces.size(); i++ )
				{
					current_center[i] = Point( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );
					int minimum_index=0;
					Rect ROI = Rect( faces[i].x - 0.25*faces[i].width, faces[i].y - 0.25*faces[i].height , 1.5*faces[i].width, 1.5* faces[i].height);
					imshow("ROI"+i, frame_gray(ROI));

					if(!firstTime)
					{						
						double minimum_deviation = cv::norm(current_center-previous_center);
										
						for(int j=0; j<faces.size(); j++)
						{	
							double deviation= cv::norm(current_center[i]-previous_center[j]);
							cout<<deviation<<endl;	
							if(deviation<=minimum_deviation)
							{
								minimum_deviation=deviation;
							
								minimum_index = j;
								
							}
						}
									
						if (minimum_index==0)				
						{
							imwrite(person0+std::to_string(p0)+".jpg", frame_gray(ROI) );
							p0++;
						}
						if(minimum_index==1)
						{
							imwrite(person1+std::to_string(p1)+".jpg", frame_gray(ROI) );
							p1++;	
						}
						if(minimum_index==2)
						{
							imwrite(person2+std::to_string(p2)+".jpg", frame_gray(ROI) );
							p2++;
						}
						if(minimum_index==3)
						{
							imwrite(person3+std::to_string(p3)+".jpg", frame_gray(ROI) );
							p3++;
						}
						if(minimum_index==4)
						{
							imwrite(person4+std::to_string(p4)+".jpg", frame_gray(ROI) );
							p4++;
						}
						
					} 
				}	
					for(int j=0;j<faces.size();j++)
					{
						previous_center[j]=current_center[j];
 					}
			}
			else
			{ 
				printf(" --(!) No captured frame -- Break!"); 
				break; 
			}
			firstTime= false;

			int c = waitKey(10);
	
			if( (char)c == 'c' ) 
			{ 
				break;
			}
		}	
	}
	return 0;
}

void detectAndDisplay( Mat frame )
{
	std::vector<Rect> faces;
	Mat frame_gray;
	
	cvtColor( frame, frame_gray, COLOR_BGR2GRAY );
	equalizeHist( frame_gray, frame_gray  );
	
	face_cascade.detectMultiScale( frame_gray, faces, 1.1, 3, 0, Size(30, 30) );
	
	for( size_t i = 0; i < faces.size(); i++ )
  	{
    		Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );
		rectangle(frame, Point(faces[i].x,faces[i].y) , Point(faces[i].x + faces[i].width,faces[i].y + faces[i].height),155 , 1, 8, 0);
		Rect ROI = Rect( faces[i].x - 0.25*faces[i].width, faces[i].y - 0.25*faces[i].height , 1.5*faces[i].width, 1.5* faces[i].height);
    		//Mat faceROI = frame_gray( faces[i] );
		Mat faceROI=frame_gray(ROI);
		//if(faces.size()!=1)
		//detectAndDisplay(faceROI);
		imshow("FaceROI" + i, faceROI);
  	}

	imshow( window_name, frame );
}

