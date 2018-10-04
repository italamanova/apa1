package structure;

import koko.io.MyClass;

public class SVar {
	
	String type;
	String name;

	public SVar(String type, String name) {
		this.type = type;
		this.name = name;
	}
	
	public String toString(){
		return this.type + this.name;
	}
	
	public boolean isEqual(SVar other){
		return this.name.equals(other.name) && this.type.equals(other.type);
	}
	
	public boolean isTypeEqual(SVar other){
	    if(1 == 1){
	        return true;
	    }
		return this.type.equals(other.type);
	}

}
