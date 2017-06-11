I took CS2413 (data structure) in 2012 spring.  To really master something , you have to foster a habit of reflection on what you have learned. 

## Project 1

1. Implement 2 classes `AccountInfo` and `UserDB` of which the attribute and functions are already declared in class headers. UserDB has allocate 200 pointers for AccountInfo objects.
2. provide a token function to parse the char array: bit by bit copy the non-delimiter substring and return a positition as the starting point for the next substring.
3. Basically, it is 4-level decision process. The last level is implemented by  `switch`  and hard coded various scenarios for adding user and its detailed information
4. implement other user methods.

## Project 2

1. **implement a vector** yourself from scratch. The key step is: when the current size is full, use new **pointer array** to allocate more memory, copy old pointers.

   ```c++
   Object* paNew=new Object[capacity]; //allocate more
   for (int i=0;i<len;i++) {
     paNew[i]=paObject[i]; // copy pointers 
   }
   delete[] paObject;
   paObject= paNew; // reassign pointer
   _size=capacity;
   ```

2. impement 2 classes: GroupDB (use vector to dynamically add Groups, match group by going through all groups and add user to found group) and GroupInfo (use vector to dynamically add user).

## project 3

1. implement a linked list from scratch.

## project 4

1. use tree structure to store English words

## project 5

compare merge sort, shellsort, adaptive sort, quicksort.