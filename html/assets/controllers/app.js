var app = angular.module('app',
	[ 'ngRoute'
		]);

app
.controller(
	'appController',
	function($rootScope, $scope, $http) 
	{
        //Agent nieruchomości
        $rootScope.user = {};
        $scope.devices = {};
        
        $scope.logindetail = {};
        
        $scope.isConnected = false;
        
        $rootScope.settings = {
            login: false,
            url: "http://127.0.0.1:5502"
        };
        
        $scope.blescan_list = {};
        
        $scope.initVars = function()
        {
            if(!$rootScope.settings.login){
                document.location = "/#/login";
            }
            $scope.checkConnection();
        }
        
        $scope.checkConnection = function() {
            $http
                .post($rootScope.settings.url + "/api/checkconnection")
				.then(
					function(result) 
					{
                        if(result.data.status == 'none'){
                            $scope.isConnected = false;
                        }
                        if(result.data.status == 'conn'){
                            $scope.isConnected = true;
                        }
					});
        }
        
        $scope.connect = function() {
            $http
                .post($rootScope.settings.url + "/api/connect")
				.then(
					function(result) 
					{
                        if(result.data.status == 'OK'){
                            $scope.checkConnection();
                            $rootScope.showSuccessAlert("Połączono!");
                        }
					});
        }
        
        $scope.disconnect = function() {
            $http
                .post($rootScope.settings.url + "/api/disconnect")
				.then(
					function(result) 
					{
                        if(result.data.status == 'OK'){
                            $scope.checkConnection();
                            $rootScope.showInfoAlert("Rozłączono!");
                        }
					});
        }
        
        $scope.blescan = function()
        {
            $http
                .post($rootScope.settings.url + "/api/blescan")
				.then(
					function(result) 
					{
                        $scope.blescan_list = result.data;
					});
        }
        
        $scope.getDevices = function()
        {
            $http
                .post($rootScope.settings.url + "/api/devices")
				.then(
					function(result) 
					{
                        $scope.devices = result.data.data;
					});
        }
        
        $scope.AddLight = function(x)
        {
            var req = {
                
                address: x.address,
                name: x.name,
                uuid: x.uuid
            }
            
            var target = '0';
            
            $http
                .post($rootScope.settings.url + "/api/add", req)
				.then(
					function(result) 
					{
                        console.log(result.data);
                        target = result.data.target;
					});
            
            /*var req2 = {
                type: "LED",
                target: target
            }
            
            $http
                .post($rootScope.settings.url + "/api/set", req)
				.then(
					function(result) 
					{
                        console.log(result.data);
                        $scope.showSuccessAlert("Dodano!");
                       // target = result.data.target;
					});*/
        }
        
        $scope.on = function(x) {
            
            var req = {
                target: x.target
            }
                            
                $http
                .post($rootScope.settings.url + "/api/on", req)
				.then(
					function(result) 
					{
                        console.log(result.data);
                        $scope.showSuccessAlert("ON!");
					});
                          
        }
        
        $scope.off = function(x) {
            
            var req = {
                target: x.target
            }
                
                $http
                .post($rootScope.settings.url + "/api/off", req)
				.then(
					function(result) 
					{
                        console.log(result.data);
                        $scope.showSuccessAlert("OFF!");
					});
                          
        }
        
        $scope.DelLight = function(x) {
            
        }
        
        $scope.EditLight = function(x) {
            
        }
        
        $scope.login = function(){
            
            var req = 
                {					
					login : $scope.logindetail.login,
                    pass: $scope.logindetail.pass
					
                };
                
            $http
                .post($rootScope.settings.url + "/api/login", req)
				.then(
					function(result) 
					{
                        if(result.data.data[0].login){
                            $rootScope.user = result.data.data[0];
                            $rootScope.settings.login = true;
                            $rootScope.showSuccessAlert("Zalogowano!");
                            document.location = "/#/start";
                        } else {
                            $rootScope.showErrorAlert("Ups! Coś poszło nie tak...");
                        }
					});
        }
        
        $scope.logout = function(){
            $rootScope.settings.login = false;
            document.location = "/#/login";
            $rootScope.showInfoAlert("Wylogowano");  
        }      
            
        //Alerty
        $rootScope.showSuccessAlert = function(text)
        {
            $(function () {
                 swal({
                    type: 'success',
                    title: text,
                    showConfirmButton: false,
                    timer: 1500
                })
            });  
        }

        $rootScope.showInfoAlert = function(text)
        {
            $(function () {
                swal({
                    type: 'info',
                    title: text,
                    showConfirmButton: false,
                    timer: 1500
                })
            });  
        }

        $rootScope.showErrorAlert = function(text)
        {
            $(function () {
             swal({
                 type: 'error',
                 title: text,
                 showConfirmButton: false,
                 timer: 1500
              })
             });  
        }
            


    });

