#include<iostream>
using namespace std;

#define MIN(a,b) a<b?a:b
#define MAX(a,b) a>b?a:b

struct range {
        int low, high;
        range() {}
        range(int l, int h): low(l),high(h) {} 
};

struct treenode {
        range r;
        int max;
        range *remove;
        treenode *left, *right;
};

void inorder(treenode *root)
{
    if (root == NULL) return;
    inorder(root->left);
    cout << "[" << root->r.low << ", " << root->r.high << "]";
    inorder(root->right);
}  

bool doOverlap(range i,range j)
{
    return (i.low <= j.high && j.low <= i.high);
} 

void updatetree(treenode *root, int l, int u)
{
    if (root == NULL) return;
    if ( doOverlap(root->r, range(l,u))) {
            root->remove = new range(l,u);
            return;
    }
    updatetree(root->left,l,u);
    updatetree(root->right,l,u);
}

treenode *newNode(range rvalue) {
     treenode *tn = new treenode;
     tn->r = range(rvalue.low, rvalue.high);
     tn->remove = NULL;
     tn->max = rvalue.high;
     tn->left=tn->right=NULL;
     return tn;
}

   
  
treenode *insertToIt(treenode *root, range rv) {
    if (!root) 
        return newNode(rv);

    if ( doOverlap(root->r, rv)) 
        root->r = range(MIN(root->r.low, rv.low), MAX(root->r.high, rv.high));
    else {    
        if(root->r.low >= rv.low) 
             root->left =  insertToIt(root->left, rv);
        else 
             root->right =  insertToIt(root->right, rv);  
    }
    return root;
    }
 

 
range QueryRange(treenode *root, int lower, int upper)
{
    if(!root) return range(-1,-1);
    if(root->r.low <= lower && root->r.high >= upper) {
        if ( root->remove) {
            if (doOverlap(*(root->remove), range(lower, upper)))
               return range(-1,-1);
        }
        return root->r;
    }
    if(root->left && root->left->max>= lower) 
        return QueryRange(root->left,lower, upper);
 
    return QueryRange(root->right, lower, upper);
} 
  
  
class RangeModule
{  
    treenode *root;
       
public:
    RangeModule() {
        root= NULL;
    }
    
   void addrange(int lower, int upper) {
    root=insertToIt(root, range(lower,upper));
    return;
   }

void myinorder()  {
    inorder(root);
}

bool QueryR(int l, int u) {
    range r =  QueryRange(root, l, u) ;
    cout << l << " : " << u << " : " << r.low << r.high<< endl;
}

void remove(int l, int u) {
    updatetree(root, l, u);
    return;
}

};


int main() {
    RangeModule r = RangeModule();
    r.addrange(10,180);
    r.addrange(150,200);
    r.addrange(250,500);
    
    r.myinorder();
    r.QueryR(50, 100);
    r.QueryR(180, 300);
    r.QueryR(600, 1000);
    r.remove(50,150);
    r.QueryR(50, 100);    
}
