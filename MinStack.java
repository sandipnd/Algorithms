import java.util.Stack;

/*
 * Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.

MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> Returns -3.
minStack.pop();
minStack.top();      --> Returns 0.
minStack.getMin();   --> Returns -2.

 */
public class minStack {

	
	Stack<Integer> primary;
	Stack<Integer> minstack;
	
	public minStack() {
		// TODO Auto-generated constructor stub
		primary = new Stack<Integer>();
		minstack = new Stack<Integer>();
	}
	
	public int getMinimum() {
		if ( !minstack.isEmpty())
		    return minstack.peek();
		return Integer.MIN_VALUE;
	}
	
	public void push(int value)
	{
				primary.push(value);
				if (minstack.isEmpty()) 
					minstack.push(value);
				else{
					if (value > minstack.peek()) {
						minstack.push(minstack.peek());
					}
					else {
						minstack.push(value);
					}
				}
		}
	public void  pop() {
		if(!primary.isEmpty()) {
		  minstack.pop();
		  primary.pop();
		}
     }	
	
	public int  top() {
		  return primary.peek();
     }
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		minStack mns = new minStack();
		
		
		mns.push(-2);
		mns.push(0);
		mns.push(-3);
		System.out.println(mns.getMinimum());   
		mns.pop();
		System.out.println(mns.top());     
		System.out.println(mns.getMinimum());
	}

}
