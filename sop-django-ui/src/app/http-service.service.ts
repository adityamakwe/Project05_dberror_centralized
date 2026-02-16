// import { HttpClient } from '@angular/common/http';
// import { Injectable } from '@angular/core';

// @Injectable({
//   providedIn: 'root'
// })
// export class HttpServiceService {

//   constructor(private httpClient: HttpClient) { }

//   post(endpoint: any, bean: any, callback: any) {
//     return this.httpClient.post(endpoint, bean).subscribe((data: any) => {
//       console.log('data =>', data)
//       callback(data);
//     }, (error: any) => {
//       callback(error);
//     })
//   }

//   get(endpoint: any, callback: any) {
//     return this.httpClient.get(endpoint).subscribe((data: any) => {
//       console.log('data =>', data)
//       callback(data);
//     }, (error: any) => {
//       callback(error);
//     })
//   }

// }


import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class HttpServiceService {

  constructor(private httpClient: HttpClient) {}

  post(endpoint: any, bean: any, callback: any) {
    this.httpClient.post(endpoint, bean).subscribe(
      (data: any) => {
        callback(data); // success case
      },
      (err: any) => {
        // ✅ normalize error response
        const res = err?.error && err.error.success !== undefined
          ? err.error
          : {
              success: false,
              result: { message: 'DB Server unavailable' }
            };

        callback(res);
      }
    );
  }

  get(endpoint: any, callback: any) {
    this.httpClient.get(endpoint).subscribe(
      (data: any) => {
        callback(data);
      },
      (err: any) => {
        const res = err?.error && err.error.success !== undefined
          ? err.error
          : {
              success: false,
              result: { message: 'DB Server unavailable' }
            };

        callback(res);
      }
    );
  }
}

