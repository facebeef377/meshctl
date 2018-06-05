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
            login: true,
            url: "http://127.0.0.1:5502"
        };
        
        $scope.blescan_list = {};
        
        $scope.initVars = function()
        {
            if(!$rootScope.settings.login){
                document.location = "/#/login";
            }
            $scope.checkConnection();
            if($scope.isConnected){
                $scope.getDevices();
            }
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
            $scope.checkConnection();
            $http
                .post($rootScope.settings.url + "/api/blescan")
				.then(
					function(result) 
					{
                        console.log(result.data);
                        $scope.blescan_list = result.data.devices;
					});
        }
        
        $scope.getDevices = function()
        {
            $scope.checkConnection();
            $http
                .post($rootScope.settings.url + "/api/devices")
				.then(
					function(result) 
					{
                        console.log(result.data.data);
                        $scope.devices = result.data.data;
					});
        }
        
        $scope.AddLight = function(x)
        {
            $scope.checkConnection();
            $rootScope.showLoading("Trwa dodawanie urządzenia");
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
                        $rootScope.closeLoading();
                        $rootScope.showSuccessAlert("Dodano urządzenie!");
					});
        }
        
        $scope.on = function(x) {
            $scope.checkConnection();
            
            var req = {
                target: x.target,
                power: x.power
            }
            
            console.log(req);
                            
                $http
                .post($rootScope.settings.url + "/api/on", req)
				.then(
					function(result) 
					{
                        console.log(result.data);
                        $scope.showSuccessAlert("ON!");
                        $scope.getDevices();
					});
            
                          
        }
        
        $scope.off = function(x) {
            $scope.checkConnection();
            
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
                        $scope.getDevices();
					});
                          
        }
        
        $scope.DelLight = function(x) {
            $scope.checkConnection();
        }
        
        $scope.setType = function(x) {
            $scope.checkConnection();
            
            swal({
              title: 'Wybierz typ urządzenia',
              text: "",
              type: 'info',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#33b6dd',
              confirmButtonText: 'BUTTON',
              cancelButtonText: 'LED',
              confirmButtonClass: 'btn btn-success',
              cancelButtonClass: 'btn btn-primary',
              buttonsStyling: false,
              reverseButtons: true
            }).then((result) => {
              if (result.value) {
                  
                  
                  var req = {
                    target: x.target
                }
                  
                $http
                .post($rootScope.settings.url + "/api/setbtn", req)
				.then(
					function(result) 
					{
                        swal(
                          'Zapisano jako Button'
                        )
                        $scope.getDevices();
					});
                  
                  
                  
                  
              } else if (
                // Read more about handling dismissals
                result.dismiss === swal.DismissReason.cancel
              ) {
                  
                var req = {
                    target: x.target
                }
                  
                $http
                .post($rootScope.settings.url + "/api/setled", req)
				.then(
					function(result) 
					{
                        swal(
                          'Zapisano jako LED'
                        )
                        $scope.getDevices();
					});
              }
            })
            
        }
        
        $scope.setPower = function(x) {
            
            console.log(x);
            
        }
        
        $scope.purge = function (){
            $scope.checkConnection();
            
            swal({
              title: 'Czy jesteś pewien?',
              text: "Po tej operacji cała sieć zostanie usunięta!",
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Tak, jestem pewien!'
            }).then((result) => {
              if (result.value) {
                $http
                .post($rootScope.settings.url + "/api/purge")
				.then(
					function(result) 
					{
                        $rootScope.showInfoAlert("Usunięto!");
					});
              }
            })
            
        }
        
        $scope.login = function(){
            $scope.checkConnection();
            
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
            $scope.checkConnection();
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
        
        $rootScope.showLoading = function(text)
        {
            $(function () {
             swal({
                    title: 'Czekaj!',
                    text: text,
                    onOpen: () => {
                        swal.showLoading()
                    }
                })  
             });  
        }
        
        $rootScope.closeLoading = function()
        {
            $(function () {
              swal.close();
            });  
        }
            
        
        /*/////////////////////////////////////////
        
        Timetable TMP
        
        *//////////////////////////////////////////
        
        $scope.hours = [
            {
                time: "0:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "1:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "2:00",
                pn: false,
                wt: false,
                sr: true,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "3:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "4:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "5:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "6:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "7:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "8:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "9:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "10:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "11:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "12:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "13:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "14:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "15:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "16:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "17:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "18:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "19:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "20:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "21:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "22:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "23:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            },
            {
                time: "24:00",
                pn: false,
                wt: false,
                sr: false,
                cz: false,
                pt: false,
                so: false,
                nd: false,
            }
        ];
        
        $scope.timechange = function(x,y){
            
            if(y == 'pn'){
                if($scope.hours[x].pn){
                    $scope.hours[x].pn = false;;
                } else {
                    $scope.hours[x].pn = true;
                }  
            }
            
            if(y == 'wt'){
                if($scope.hours[x].wt){
                    $scope.hours[x].wt = false;;
                } else {
                    $scope.hours[x].wt = true;
                }  
            }
            
            if(y == 'sr'){
                if($scope.hours[x].sr){
                    $scope.hours[x].sr = false;;
                } else {
                    $scope.hours[x].sr = true;
                }  
            }
            
            if(y == 'cz'){
                if($scope.hours[x].cz){
                    $scope.hours[x].cz = false;;
                } else {
                    $scope.hours[x].cz = true;
                }  
            }
            
            if(y == 'pt'){
                if($scope.hours[x].pt){
                    $scope.hours[x].pt = false;;
                } else {
                    $scope.hours[x].pt = true;
                }  
            }
            
            if(y == 'so'){
                if($scope.hours[x].so){
                    $scope.hours[x].so = false;;
                } else {
                    $scope.hours[x].so = true;
                }  
            }
            
            if(y == 'nd'){
                if($scope.hours[x].nd){
                    $scope.hours[x].nd = false;;
                } else {
                    $scope.hours[x].nd = true;
                }  
            }
            
        }


    });

