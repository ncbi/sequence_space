#ifndef LOOKUPENSEMBLID_CPP
#define LOOKUPENSEMBLID_CPP

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

map<string,string> ensemblMap;

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
		if (curWord == "-in")	// the all_hits file with UniProt column 1 and Ensembl column 2
			inFileName = argv[++i];
		else if (curWord == "-in2") // the sequences in common between Lauren's Uniprot database & the Ensembl one
			in2FileName = argv[++i];
		else if (curWord == "-out")
			outFileName = argv[++i];
	}

	ifstream infile ((char*)inFileName.c_str());
	if (!infile)	// used to read if (infile == NULL) which became deprecated!!!!
		cout << "ERROR: couldn't find file " << inFileName << endl;
	ifstream in2file ((char*)in2FileName.c_str());
	if (!in2file)	// used to read if (infile == NULL) which became deprecated!!!!
		cout << "ERROR: couldn't find file " << in2FileName << endl;
	ofstream outfile ((char*)outFileName.c_str());

	string line;

	while(getline(infile,line))
	{
		if (line == "")
			break;
		vector<string> words = split(line);
		string uniProt = words[0];
		string ensembl = words[1];
		ensemblMap[uniProt] = ensembl;
	}
	infile.close();

	while(getline(in2file,line))
	{
		if (line == "")
			break;
		string hit = ensemblMap[line];
		if (hit != "")
			outfile << hit << endl;
	}
	in2file.close();
	outfile.close();
}
			
#endif




















