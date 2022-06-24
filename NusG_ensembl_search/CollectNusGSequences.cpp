#ifndef FINDGENENAMES_CPP
#define FINDGENENAMES_CPP

#include <iostream>
#include <sstream>
#include <iomanip>
#include <fstream>
#include <string>
#include <cstdlib>
#include <vector>
#include <map>
#include <set>
#include <list>
#include <algorithm>

using namespace std;
const bool FALSE = 0;
const bool TRUE = 1;

char isSpaceOrBracketOrTabOrControlCharacterOrComma(char c)
{
	if ((c == ' ') || (c == '{') || (c == '}') || (c == '\t') || ((int)c == 13) || (c == ','))
		return TRUE;
	else
		return FALSE;
}

vector<string> split (const string& s)
{
	vector<string> ret;
	typedef string::size_type string_size;
	string_size i = 0;

	// invariant: we have processed characters in the range [original value of i,i).
	while (i != s.size())
	{
		//ignore leading blanks
		// invariant: characters in the range [i^orig,i^cur) are all spaces or brackets, etc
		while (i != s.size() && isSpaceOrBracketOrTabOrControlCharacterOrComma(s[i]))
			++i;

		// find the end of the next word
		string_size j = i;
		// invariant: none of the characters in the range [j^orig,j^cur) is a space or bracket, etc
		while (j != s.size() && !isSpaceOrBracketOrTabOrControlCharacterOrComma(s[j]))
			++j;

		// if we found some non-whitespace and non-bracket characters
		if (i != j)
		{
			// copy from s starting at i and taking j-i characters
			ret.push_back(s.substr(i,j-i));
			i = j;
		}
	}
	return ret;
}

int main(int argc, char *argv[])
{
	string inFileName,outFileName,searchSeq;
	
	for (int i = 1; i < argc; i++)
	{
		string curWord = argv[i];
		if (curWord == "-in")
			inFileName = argv[++i];
		else if (curWord == "-out")
			outFileName = argv[++i];
		else if (curWord == "-seq")
			searchSeq = argv[++i];
	}

	ifstream infile ((char*)inFileName.c_str());
	if (!infile)	// used to read if (infile == NULL) which became deprecated!!!!
		cout << "ERROR: couldn't find file " << inFileName << endl;
	ofstream outfile ((char*)outFileName.c_str());

	string line,line2,line3;

	while(getline(infile,line))
	{
		vector<string> words = split(line);
		if (line == "")
			continue;
		string curr = words[0];
		int place = curr.find_last_of('/') + 1;
		string name = curr.substr(place);
		
		outfile << name << endl;
		
		string command = "zcat " + line + " | grep -i gene | grep -i '" + searchSeq + "' > temp.log";
		system((char*)command.c_str());

		ifstream tempfile ("temp.log");
		while(getline(tempfile,line2))
		{	
			//cout << "working on line2 = " << line2 << endl;
			vector<string> words = split(line2);
			command = "zcat " + line + " | awk '/" + words[0] + "/{print;getline;print;getline;print;getline;print;getline;print;getline;print;getline;print}' > temp2.log";
			//cout << "issuing command " << command << endl;
			system((char*)command.c_str());
			int num = 0;
			string currSeq="";
			ifstream tempfile2 ("temp2.log");
			getline(tempfile2,line3);
			outfile << line3 << endl;
			while(getline(tempfile2,line3))
			{	if (line3[0] == '>')
					num++;
				if (num == 1)
					break;
				currSeq += line3;
			}
			if (currSeq != "")
				outfile << currSeq << endl;
			else
				outfile << "NONE FOUND" << endl;
			tempfile2.close();
		}
		tempfile.close();
	}
	
	infile.close();
	outfile.close();
}
			
#endif




















