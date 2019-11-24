//JS QuickSort

Array.prototype.quickSort = function() {

  var r = this;
  if(this.length <= 1) {
    return this;
  }
  var less = [], greater = [];

  var pivot = r.splice(Math.floor(r.length / 2),1);

  for (var i = r.length - 1 ; i >= 0; i--){
    if ( r[i] <= pivot) {
      less.push(r[i]);
    } else {
      greater.push(r[i]);
    }
  }
  
  var c = [];
  
return c.concat(less.quickSort(), pivot, greater.quickSort());

};

var a = [3,1,43,5,123,6,231,0];
console.log(a.quickSort());

