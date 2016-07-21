#include<iostream>
#include <queue>
#include <string.h>
#include <list>
#include <map>
#include <string>

#define CLUSTER_SIZE 3
using namespace std;

typedef enum {
    LessThan = 0,
    LessThanEquals = 1,
    Equals = 2,
    GreaterThanEquals = 3,
    GreaterThan = 4
} SearchType;

typedef enum {
    NotFound,
    FoundExact,
    FoundGreater,
    FoundLess
} SearchResult;


typedef struct kvmap {
    int value;
    int index;
}kvmap; 

/*

My logic :  Here the operations >, = ,<, >= , <= 
            These operations are very similar as 
            qpart from = , rest of opeartors tries to find
            max or minimum value around the key .
            lets assume arr =[ 0,2,4,6,8]
            Here greaterthanequals 4 is 6 , less than equalto is 6
            Always there is a cluster around it

            The cluster size is always 3. Trying to do a sliding window concept
            to hold the cluster of 3 values.  The answer will always lie between this
             
For Production:
            if we have this API search , this API will create a list ( each element is a structure containing value and index)
            The list will have Max 3 entries, so conditonal loop on three element will be faster. 
            Both of those will be send to a task queue to execute and publish result.


*/



SearchResult processcluster(const int key, const SearchType type ,  list<kvmap> *mymap, int* const index) {
    /*
      Here we will find element in list and check. 
      The list will contain three values , lets assume list contains 3 values [ a,x,b] key = x
      As there is no duplicate , so a < x , b > x 
      a is nearest less than , b is just greater .

    */
    SearchResult result = NotFound;
    int tmpindex;

    /*display the cluster
     cout << "cluster value \n";
     for ( list<kvmap>::iterator it = mymap->begin(); it != mymap->end(); ++it) {
          kvmap tmp = *it;
          cout << tmp.value << "  ";
     }
     */
    
    for ( list<kvmap>::iterator it = mymap->begin(); it != mymap->end(); ++it) {
       kvmap tmp = *it;
       switch(type) {
          case LessThan:
            // for less than First value is needed
            
            if ( key > tmp.value ) {
               tmpindex = tmp.index;
               result =  FoundLess;
            }                
            break;
         case LessThanEquals:
            if ( key > tmp.value  ) {
               tmpindex = tmp.index;
               result = FoundLess;
             } 
            if (key == tmp.value) {
               tmpindex = tmp.index;
               result = FoundExact;
            }
            break;
        case Equals:
            if ( tmp.value == key ) {
               tmpindex = tmp.index;
               result = FoundExact;
            }
            break;              
       case GreaterThanEquals:
            /*
              Once a match is found , rest no need to check
             */ 
            if ( key < tmp.value  && (result != FoundExact)) {
               tmpindex = tmp.index;
               result = FoundGreater;
            } 
            if (key == tmp.value) {
               tmpindex = tmp.index;
               result = FoundExact;
            }
            break;
        case GreaterThan:
            if ( key < tmp.value ) {
               tmpindex = tmp.index;
               result =  FoundGreater;
            }                
            break;
            
     }
   }
     if ( result != NotFound) 
         memcpy(index,&tmpindex,sizeof(int));

     delete(mymap); 
     return result;
}

void processmap(list<kvmap> *mymap, int key, int value) {
    /*
      This function will create a list. The list here acts as Queue.
      Always maintain a max size of 3
    */

     kvmap tmp;
     tmp.value =  key;
     tmp.index = value;

     if ( mymap->size() == CLUSTER_SIZE )
        mymap->pop_front();

     mymap->push_back(tmp);
}

SearchResult process( const int * const items , int ascending, 
                            int* const index, const SearchType type , 
                               const int key, const int n_items) {

   list<kvmap> *mymap = new list<kvmap>;
   if (mymap == NULL) {
     cout << "Error in memory allocation: Exiting";
     return NotFound;
   }

   int spointer  = ( ascending == 1)? 0: n_items-1;
   int incrdcr = ( ascending == 1)? 1:-1; // what value to use to increment or decrement
   
   /*
    This part of code common for both asc and desc,
    As the pointer starts from either 0 or end
   */
   while (items[spointer] <= key && (spointer < n_items && spointer >= 0)) {
            processmap(mymap,items[spointer],spointer);
            spointer += incrdcr; // either +1 or -1 
    }
    if (( ascending == 1) &&  spointer < n_items) //adding next biggest value
        processmap(mymap,items[spointer],spointer);

    if (( ascending == 0) && spointer > 0) //adding next smaller value
        processmap(mymap,items[spointer],spointer);
  
    return processcluster(key, type, mymap, index);
}



SearchResult Search(
    const int * const items,
    const int n_items,
    const int ascending,
    const int key,
    const SearchType type,
    int* const index)
{
  return process(items, ascending, index,type, key,n_items);
}


void display(int result , int index, int key) {
    /*
    This test purpose

    */
    cout << "====  result is : "<< result << '\n' ;
    cout << "index = " << index << " for key = " << key << "  ====\n\n\n";
}

void ascendingtest() {

  int arr[5] = {0,2,4,6,8};
  int index = -1;
  int result ;

  cout << " == ASCENDING TEST == \n\n";
  cout << "-9999 lessthanequals\n";
  result = Search(arr,5,1, -9999, LessThanEquals, &index);
  display(result, index, -9999);

  cout << "-1 lessthanequals\n";
  result = Search(arr,5,1, -1, LessThanEquals, &index);
  display(result, index, -1);

  cout << "0 less than\n";
  index = -1;
  result = Search(arr,5,1, 0, LessThan, &index);
  display(result, index, -1);


  cout << "4 less than\n";
  index = -1;
  result = Search(arr,5,1, 4, LessThan, &index);
  display(result, index, 4);


  cout << "0 equals\n";
  index = -1;
  result = Search(arr,5,1, 0, Equals, &index);
  display(result, index, 0);

  cout << "1 Equals \n";
  index = -1;
  result = Search(arr,5,1, 1, Equals, &index);
  display(result, index, 1);

  cout << "2 GreaterThanEquals\n";
  index = -1;
  result = Search(arr,5,1, 2, GreaterThanEquals, &index);
  display(result, index, 2);

  cout << "2 greaterthan\n";
  index = -1;
  result = Search(arr,5,1, 2, GreaterThan, &index);
  display(result, index, 2);

  cout << "10 greaterthan\n";
  index = -1;
  result = Search(arr,5,1, 10, GreaterThan, &index);
  display(result, index, 10);

  cout << "9999 greaterthan\n";
  index = -1;
  result = Search(arr,5,1, 9999, GreaterThan, &index);
  display(result, index, 9999);

  cout << "7 equals \n";
  index = -1;
  result = Search(arr,5,1, 7, Equals, &index);
  display(result, index, 7);

  cout << "8 equals \n";
  index = -1;
  result = Search(arr,5,1, 8, Equals, &index);
  display(result, index, 8);

  cout << "8 greaterthan\n";
  index = -1;
  result = Search(arr,5,1, 8, GreaterThan, &index);
  display(result, index, 8);

  cout << "5 GreaterThanEquals\n";
  index = -1;
  result = Search(arr,5,1, 5, GreaterThanEquals, &index);
  display(result, index, 5);

  cout << "5 GreaterThan\n";
  index = -1;
  result = Search(arr,5,1, 5, GreaterThan, &index);
  display(result, index, 5);

  cout << "5 LessThan\n";
  index = -1;
  result = Search(arr,5,1, 5, LessThan, &index);
  display(result, index, 5);

}

void descendingtest() {

  int arr[5] = {8,6,4,2,0};
  int index = -1;
  int result ;

  cout << " == DESCENDING TEST == \n";

  cout << "-9999 lessthanequals\n";
  result = Search(arr,5,0, -9999, LessThanEquals, &index);
  display(result, index, -9999);

  cout << "-1 lessthanequals\n";
  result = Search(arr,5,0, -1, LessThanEquals, &index);
  display(result, index, -1);

  cout << "0 less than\n";
  index = -1;
  result = Search(arr,5,0, 0, LessThan, &index);
  display(result, index, -1);


  cout << "4 less than\n";
  index = -1;
  result = Search(arr,5,0, 4, LessThan, &index);
  display(result, index, 4);


  cout << "0 equals\n";
  index = -1;
  result = Search(arr,5,0, 0, Equals, &index);
  display(result, index, 0);

  cout << "1 Equals \n";
  index = -1;
  result = Search(arr,5,0, 1, Equals, &index);
  display(result, index, 1);

  cout << "2 GreaterThanEquals\n";
  index = -1;
  result = Search(arr,5,0, 2, GreaterThanEquals, &index);
  display(result, index, 2);

  cout << "2 greaterthan\n";
  index = -1;
  result = Search(arr,5,0, 2, GreaterThan, &index);
  display(result, index, 2);

  cout << "10 greaterthan\n";
  index = -1;
  result = Search(arr,5,0, 10, GreaterThan, &index);
  display(result, index, 10);

  cout << "9999 greaterthan\n";
  index = -1;
  result = Search(arr,5,0, 9999, GreaterThan, &index);
  display(result, index, 9999);

  cout << "7 equals \n";
  index = -1;
  result = Search(arr,5,0, 7, Equals, &index);
  display(result, index, 7);

  cout << "8 equals \n";
  index = -1;
  result = Search(arr,5,0, 8, Equals, &index);
  display(result, index, 8);

  cout << "8 greaterthan\n";
  index = -1;
  result = Search(arr,5,0, 8, GreaterThan, &index);
  display(result, index, 8);

  cout << "5 GreaterThanEquals\n";
  index = -1;
  result = Search(arr,5,0, 5, GreaterThanEquals, &index);
  display(result, index, 5);

  cout << "5 GreaterThan\n";
  index = -1;
  result = Search(arr,5,0, 5, GreaterThan, &index);
  display(result, index, 5);

  cout << "5 LessThan\n";
  index = -1;
  result = Search(arr,5,0, 5, LessThan, &index);
  display(result, index, 5);

}

int main() {
      ascendingtest();
     //descendingtest();
}
