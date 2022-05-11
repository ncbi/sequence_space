#ifndef COMBINENUSG_SECE_CPP
#define COMBINENUSG_SECE_CPP

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
	string inFileName,in2FileName,outFileName;
	
	for (int i = 1; i < argc; i++)
	{
		string curWord = argv[i];
		if (curWord == "-in")
			inFileName = argv[++i];
		else if (curWord == "-in2")
			in2FileName = argv[++i];
		else if (curWord == "-out")
			outFileName = argv[++i];
	}

	ifstream infile ((char*)inFileName.c_str());
	if (!infile)	// used to read if (infile == NULL) which became deprecated!!!!
		cout << "ERROR: couldn't find file " << inFileName << endl;
	ofstream outfile ((char*)outFileName.c_str());

	string line,line2;

	while(getline(infile,line))
	{
		vector<string> words = split(line);
		//outfile << species << endl;

		string assembly = words[2];
		int firstPlace1 = assembly.find_last_of(':') + 1;
		string firstFrameString = assembly.substr(firstPlace1);
		int firstFrame = atoi((char *)firstFrameString.c_str());
		string firstSub1 = assembly.substr(0,firstPlace1 - 1);

		int firstPlace2 = firstSub1.find_last_of(':') + 1;
		string firstEndString = firstSub1.substr(firstPlace2);
		int firstEnd = atoi((char *)firstEndString.c_str());
		string firstSub2 = firstSub1.substr(0,firstPlace2 - 1);

		int firstPlace3 = firstSub2.find_last_of(':') + 1;
		string firstStartString = firstSub2.substr(firstPlace3);
		int firstStart = atoi((char *)firstStartString.c_str());
		string firstSub3 = firstSub2.substr(0,firstPlace3 - 1);

		string command = "grep " + firstSub3 + ": " + in2FileName + " > temp.log";
		system((char*)command.c_str());

		int matches = 0;
		int closestDistance = 999999;
		int cutOff = 9999;
		int bestStart,bestEnd,bestFrame;

		ifstream tempfile ("temp.log");
		while(getline(tempfile,line2))
		{	
			if (line2 == "")
				break;

			vector<string> words2 = split(line2);
			string match = words2[2];

			int matchPlace1 = match.find_last_of(':') + 1;
			string matchFrameString = match.substr(matchPlace1);
			int matchFrame = atoi((char *)matchFrameString.c_str());
			string matchSub1 = match.substr(0,matchPlace1 - 1);

			int matchPlace2 = matchSub1.find_last_of(':') + 1;
			string matchEndString = matchSub1.substr(matchPlace2);
			int matchEnd = atoi((char *)matchEndString.c_str());
			string matchSub2 = matchSub1.substr(0,matchPlace2 - 1);

			int matchPlace3 = matchSub2.find_last_of(':') + 1;
			string matchStartString = matchSub2.substr(matchPlace3);
			int matchStart = atoi((char *)matchStartString.c_str());
			string matchSub3 = matchSub2.substr(0,matchPlace3 - 1);

			int startDiff = firstStart - matchStart;
			int endDiff   = firstEnd   - matchEnd;
			//outfile << match << endl << startDiff << "\t" << endDiff << "\t" << firstFrame << " " << matchFrame << endl;
			if (abs(startDiff) < closestDistance)
			{
				closestDistance = abs(startDiff);
				bestStart = matchStart;
				bestEnd = matchEnd;
				bestFrame = matchFrame;
			}
			matches++;
		}
		if (closestDistance < cutOff)
		{	outfile << line << "(YES NusG: " << closestDistance << " from " << bestStart << " " << bestEnd << ")";
			if (bestFrame != firstFrame)
				outfile << " (Different frames NusG, L11)";
			outfile << endl;
		}
		else if (matches == 0)
		{	outfile << line << "(NO L11 found)" << endl;
		}
		else
			outfile << line << "(NOT NUSG)" << endl;

		tempfile.close();

		getline(infile,line);
		outfile << line << endl;
	}
	
	infile.close();
	outfile.close();
}
			
#endif




















