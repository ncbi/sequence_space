#ifndef CLEANUPFASTAFILE_CPP
#define CLEANUPFASTAFILE_CPP

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
	string inFileName,outFileName;
	
	for (int i = 1; i < argc; i++)
	{
		string curWord = argv[i];
		if (curWord == "-in")
			inFileName = argv[++i];
		else if (curWord == "-out")
			outFileName = argv[++i];
	}

	ifstream infile ((char*)inFileName.c_str());
	if (!infile)	// used to read if (infile == NULL) which became deprecated!!!!
		cout << "ERROR: couldn't find file " << inFileName << endl;
	ofstream outfile ((char*)outFileName.c_str());

	string line;

	while(getline(infile,line))
	{
		string name = line;
		for (int i = 0; i < 10; i++)
		{	char c = infile.peek();
			if (c != '>')
				break;
			getline(infile,line);
			string annotation = line;
			getline(infile,line);
			string seq = line;
			outfile << annotation << "(" << name << ")" << endl << seq << endl;
		}
	}
	
	infile.close();
	outfile.close();
}
			
#endif




















