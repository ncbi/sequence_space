#ifndef MERGEFASTAFILES_CPP
#define MERGEFASTAFILES_CPP

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
	ifstream in2file ((char*)in2FileName.c_str());
	if (!in2file)	// used to read if (infile == NULL) which became deprecated!!!!
		cout << "ERROR: couldn't find file " << in2FileName << endl;
	ofstream outfile ((char*)outFileName.c_str());

	string line,line2,name1,seq1,name2,seq2,species;

	while(getline(infile,line))
	{
		getline(in2file,line2);
		species = line;
		outfile << species << endl;

		getline(infile,line);
		if (line != "NONE FOUND")
		{	name1 = line;
			getline(infile,line);
			seq1 = line;
		}
		else
			seq1 = "NONE FOUND";

		getline(in2file,line2);
		if (line2 != "NONE FOUND")
		{	name2 = line2;
			getline(in2file,line2);
			seq2 = line2;
		}
		else
			seq2 = "NONE FOUND";

		if (seq1 == "NONE FOUND" && seq2 != "NONE FOUND")
			outfile << name2 << endl << seq2 << endl;
		else if (seq2 == "NONE FOUND" && seq1 != "NONE FOUND")
			outfile << name1 << endl << seq1 << endl;
		else if (seq1 != "NONE FOUND" && seq1 != "NONE FOUND")
		{	if (seq1 != seq2)
				outfile << name1 << endl << seq1 << endl << endl << species << name2 << endl << seq2 << endl;
			else
				outfile << name1 << endl << seq1 << endl;
		}
		else if (seq1 == "NONE FOUND" && seq2 == "NONE FOUND")
			outfile << "NONE FOUND" << endl;
		outfile << endl;
	}
	
	infile.close();
	in2file.close();
	outfile.close();
}
			
#endif




















