package com.walter.fizzbuzz.enumeration;

public enum FizzBuzzStratageEnum {

	/**
	 * append all IntegerToStringService transfer result in ASC order
	 */
	APPEND_ALL_ASC("APPEND_ALL_ASC"),
	
	/**
	 * append all IntegerToStringService transfer result in DESC order
	 */
	APPEND_ALL_DESC("APPEND_ALL_DESC");
	
	private String code;
	
	private FizzBuzzStratageEnum(String code) {
		this.code = code;
	}

	public String getCode() {
		return code;
	}
}
