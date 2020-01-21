// Olivia Zhang, P-Set 3, Recover

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // ensure the user inputs exactly 2 arguments (1 command-line argument)
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ForensicFileName\n");
        return 1;
    }

    // initialize char array of arrays to store names of the new jpeg files
    char jpegfilenames[50][6];
    // initialize a counter that keeps track of how many jpeg files have been recovered at a given moment
    int jpegfilenumber = 0;
    FILE *img = NULL;
    // initialize the temporary variable for every loop the current 512 block is read and stored
    unsigned char arrayelement[512];

    // open memory card file from which to recover JPEGs file and say error if it does not exist
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    // conditions to read the memory file and then outpul to jpeg files accordingly
    while (fread(arrayelement, 512, 1, file) == 1)
    {
        // condition for if the start of a jpeg file has been reached
        if (arrayelement[0] == 0xff && arrayelement[1] == 0xd8 && arrayelement[2] == 0xff && (arrayelement[3] & 0xf0) == 0xe0)
        {
            // not the first jpeg file created
            if (jpegfilenumber != 0)
            {
                fclose(img);
                sprintf(jpegfilenames[jpegfilenumber], "%03i.jpg", jpegfilenumber);
                img = fopen(jpegfilenames[jpegfilenumber], "w");
                fwrite(&arrayelement, 512, 1, img);
            }

            // open the first jpeg
            else if (jpegfilenumber == 0)
            {
                sprintf(jpegfilenames[jpegfilenumber], "%03i.jpg", jpegfilenumber);
                img = fopen(jpegfilenames[jpegfilenumber], "w");
                // write 512 bytes until new JPEG is found
                fwrite(&arrayelement, 512, 1, img);
            }
            jpegfilenumber++;
        }
        // the blocks in the middle of the jpeg files, i.e. not the starting blocks
        else
        {
            if (jpegfilenumber > 0 && jpegfilenumber <= 50)
            {
                fwrite(&arrayelement, 512, 1, img);
            }
        }
    }
    // close file
    fclose(file);
    return 0;
}