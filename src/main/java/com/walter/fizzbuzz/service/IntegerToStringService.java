package com.walter.fizzbuzz.service;

public interface IntegerToStringService {
	
	/**
	 * To transfer integer n into string that it stands for.
	 * @param n
	 * @return
	 */
	public String transfer(int n);
	
	/**
	 * To determine whether an input integer n can be transferred into string that it stands for.
	 * @param n
	 * @return
	 */
	public boolean support(int n);
}
