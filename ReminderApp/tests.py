from django.test import TestCase

# Create your tests here.

'''import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';
import {Data} from './loginData';
import {map} from 'rxjs/operators';
import {Route} from '@angular/router';

@Injectable({
  providedIn: 'root'
})


export class SignupService {

  private currentUserSubject: BehaviorSubject<Data>;
  public currentUser: Observable<Data>;

  constructor(private http: HttpClient, private route: Route) {
    this.currentUserSubject = new BehaviorSubject<Data>(JSON.parse(localStorage.getItem('currentUser')));
    this.currentUser = this.currentUserSubject.asObservable();
  }
  signup(username, password) {

    // tslint:disable-next-line:variable-name
    const req_obj = {"username": username,"password": password};
    const body = JSON.stringify(req_obj);
    return this.http.post<any>(`http://127.0.0.1:8000/signup/`, body)
      .pipe(map(user => {           
        // tslint:disable-next-line:new-parens
        return user ;
      }));
  }

}
'''