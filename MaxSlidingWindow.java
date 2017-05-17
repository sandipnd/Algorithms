import java.util.Deque;
import java.util.LinkedList;

public class maxsliding {

	public maxsliding() {
		// TODO Auto-generated constructor stub
	}

	public static void  maxslide() {
		Deque<Integer> de = new LinkedList();
		int var[] = {-7,-8,7,5,7,1,6,0}; //{ 5,3,4,1,6,2,2,4,3,1,5};
		int start = 0;
		int k = 4;
		int[] output = new int[var.length - k  +1];
		int index = 0;
		for(int i = 0; i < var.length; i++) {
			
			if (de.isEmpty()) {
				de.add(i); //5
				//continue;
			}
			if ( var[i] < var[de.getLast()]) {
				de.addLast(i);  //5 3 
			}
			else {
				while (!de.isEmpty() && var[i] >= var[de.getLast()])
					de.removeLast();  //5 4
				de.add(i);
			}
			//System.out.println(de);
			
			if (i >=  k) {
			   //System.out.println(var[de.getFirst()]);
			   output[index++] = var[de.getFirst()];
			   if (de.getFirst() == start ) {
				   de.removeFirst();
			   }
			   start ++;
			}
			
		}
		
		
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
         maxsliding.maxslide();
	}

}
