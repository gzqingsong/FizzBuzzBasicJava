package com.walter.fizzbuzz.exception;

public class FizzBuzzException extends RuntimeException {

	private static final long serialVersionUID = 1L;
	
	public FizzBuzzException(String message) {
		super(message);
	}
}
