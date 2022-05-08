package rules_test

import data.rules.allow as allow

test_car_read_positive {
	in = {
		"method": "GET",
		"path": ["cars"],
		"user": "alice",
	}

	allow == true with input as in
}

test_car_read_negative {
	in = {
		"method": "GET",
		"path": ["nonexistent"],
		"user": "alice",
	}

	allow == false with input as in
}

test_car_create_negative {
	in = {
		"method": "POST",
		"path": ["cars"],
		"user": "alice",
	}

	allow == false with input as in
}

test_car_create_positive {
	in = {
		"method": "POST",
		"path": ["cars"],
		"user": "charlie",
	}

	allow == true with input as in
}
