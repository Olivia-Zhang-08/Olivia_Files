// Olivia Zhang, P-Set 4, Hash Table Spellcheck
// Thank you Bill for Office Hours!!

// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <cs50.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define numbuckets 10000

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[numbuckets];

// Initialize size count
unsigned int count = 0;

// Hash function obtained from:
// https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c
unsigned int hash(const char *word)
{
    unsigned long hashnum = 5381;
    for (const char* ptr = word; *ptr != '\0'; ptr++)
    {
        hashnum = ((hashnum << 5) + hashnum) + tolower(*ptr);
    }
    return hashnum % numbuckets;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < numbuckets; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));

        // Malloc returns NULL if you run out of memory
        // If the pointer to the new node returns NULL, then unload dictionary and return false to quit speller
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // Copy current word into new node
        strcpy(new_node->word, word);

        // Insert new node at beginning of linked list:
        // Make the new node point to what the root is also pointing to
        // Then make the root point to new node
        new_node->next = hashtable[hash(word)];
        hashtable[hash(word)] = new_node;
        count++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *cursor = hashtable[hash(word)];
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < numbuckets; i++)
    {
        node *cursor = hashtable[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
