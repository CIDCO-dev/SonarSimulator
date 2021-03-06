/*
* Copyright 2019 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
*/

#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <iomanip>
#include <csignal>

/* 
 * File:   simulate-sonar.hpp
 * Author: emile
 *
 * Created on June 26, 2019, 2:41 PM
 */

class SonarSimulator
{
    public:
        
        SonarSimulator(double frequenceHertz, double pattern, std::string & filename, std::string talkerID = "SD"):
        frequenceHertz(frequenceHertz),
        depthPattern(pattern),
        outputFilename(filename),
        talkerID(talkerID)
        {}
        
        ~SonarSimulator()
        {}
        
        void setFrequence(double frequenceHertz)
        {
            frequenceHertz = frequenceHertz;
        }
        
        void setDepthPattern(double pattern)
        {
            depthPattern = pattern;
        }
        
        void setOutputFilename(std::string & fileName)
        {
            outputFileName = fileName;
        }
        
        void run()
        {
            if (frequenceHertz > 0)
            {
	        outputFile.open(outputFileName);
		
		if(outputFile){
			while(1)
			{
			    usleep(1000000/frequenceHertz); 
			    double depth = 3.75;
			    outputFile << generateNMEA(depth);
			}
		}
		else{
			throw new std::exception("Output file not found");
		}
            }
            else
            {
		throw new std::out_of_range("Frequency cannot be negative");
            }
        }
        
        std::string generateNMEA(double depth)
        {
            std::stringstream nmea;
            double ftDepth = depth*3.28084;
            double fmDepth = ftDepth/6;
            nmea << std::setprecision(1) << std::fixed;
            nmea << "$" << talkerID << "DBT," << ftDepth << ",f," << depth << ",M," << fmDepth << ",F" << "*";
            int checksum = 0;
            for (int i = 1; i < (int)nmea.str().length()-1; i++)
            {
                checksum ^= nmea.str().c_str()[i];
            }
            nmea << std::hex << checksum << "\x0d\x0a";
            return nmea.str();
        }
        
        void closeFile()
        {
            outputFile.close();
        }
        
    private:
        
        double frequenceHertz;
        
        double depthPattern;
        
        std::string outputFilename;
        
        std::ofstream outputFile;
        
        std::string talkerID;
        
};

void printUsage()
{
    std::cerr << "Usage: simulate-sonar outputFileName" << std::endl;
	exit(1);
}

SonarSimulator *simulator;

void closeProgram(int signum)
{
    simulator->closeFile();
    exit(1);
}

int main(int argc,char **argv)
{
    signal(SIGINT,closeProgram);
    if (argc == 2)
    {    
        std::string filename = argv[1];
        simulator = new SonarSimulator(0.5,10,filename);
        simulator->run();
    }
    else
    {
        printUsage();
    }
}
