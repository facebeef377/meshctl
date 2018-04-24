app.config(function($routeProvider,$locationProvider) {
	$locationProvider.hashPrefix('');
	$routeProvider	
    .when('/start', {
		templateUrl : 'parts/dashboard.html',
	})
    .when('/add', {
		templateUrl : 'parts/device_add.html',
	})
    .when('/list', {
		templateUrl : 'parts/device_list.html',
	})
    .when('/login', {
		templateUrl : 'parts/login.html',
	})
	.otherwise({
		redirectTo : '/start'
	});
});