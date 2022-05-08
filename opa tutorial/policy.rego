package rules

default allow = false

users := {
	"alice": {
		"manager": "charlie",
		"title": "salesperson",
	},
	"bob": {
		"manager": "charlie",
		"title": "salesperson",
	},
	"charlie": {
		"manager": "dave",
		"title": "manager",
	},
	"dave": {
		"manager": null,
		"title": "ceo",
	},
}

user_is_employee {
	users[input.user]
}

user_is_manager {
	users[input.user].title != "salesperson"
}

allow {
	input.method == "GET"
	input.path == ["cars"]
}

allow {
	# only managers can create a new car
	input.method == "POST"
	user_is_manager
	input.path == ["cars"]
}

allow {
	# only employees can GET /cars/{carid}
	user_is_employee
	carid := input.path[1]
	input.path == ["cars", carid]
	input.method == "GET"
}
