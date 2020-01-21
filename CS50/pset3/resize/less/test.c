// Resizes a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <cs50.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure the user inputs exactly 4 arguments (3 command-line arguments)
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize infile outfile\n");
        return 1;
    }

    // ensure that the first command-line argument is a positive integer <= 100 (this is the scale factor)
    for (int t = 0, n = strlen(argv[1]); t < n; t++)
    {
        if (!isdigit(argv[1][t]) || argv[1][t] <= 0 || argv[1][t] > 100)
        {
            fprintf(stderr, "Usage: resize infile outfile\n");
            return 2;
        }
    }

    // remember filenames
    int scale = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

 // determine padding for scanlines
    int paddingbefore = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    int imgwidthbefore = bi.biWidth;
    int imgheightbefore = bi.biHeight;

    bi.biWidth *= scale;
    bi.biHeight *= scale;

    int paddingafter = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = ((3 * bi.biWidth) + paddingafter) * abs(bi.biHeight);
    bf.bfSize = 54 + bi.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(imgheightbefore); i < biHeight; i++)
    {

            // iterate over pixels in scanline
            for (int k = 0; k < imgwidthbefore; k++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);


                // write RGB triple to outfile
                for (int m = 0; m < scale; m++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // skip over padding, if any
            fseek(inptr, paddingbefore, SEEK_CUR);


            // then add it back (to demonstrate how)
            for (int n = 0; n < paddingafter; n++)
            {
                fputc(0x00, outptr);
            }

            //fseek(inptr, -(imgwidthbefore * 3 + paddingbefore), SEEK_CUR);
            //fseek(inptr, 1, SEEK_CUR);

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
