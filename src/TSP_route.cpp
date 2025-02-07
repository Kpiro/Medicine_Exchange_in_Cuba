#include <bits/stdc++.h>
using namespace std;

// Función recursiva para calcular el costo mínimo y la ruta
int totalCost(int mask, int curr, int m, 
              vector<vector<int>> &cost, vector<vector<int>> &memo, 
              vector<vector<int>> &path, vector<int> &cicle) {

    // Base case: si todos los productos fueron entregados en sus respectivos lugares, 
    // devolver el costo de regresar al origen (0)
    int n = (m+1)/2;
    if (mask == (1 << m) - 1) {
        path[curr][mask]=0;
        return cost[curr][0];
    }

    // Si el resultado ya está en la memoización, devolverlo
    if (memo[curr][mask] != -1)
        return memo[curr][mask];

    

    int ans = INT_MAX;
    int nextCity = -1;

    // Intentar visitar cada lugar que no ha sido visitado aún
    for (int i = 0; i < m; i++) {
        int city = i<n ? i : ((i%n)+1);

        if((  ( (mask & (1 << i) )==0) and (i<n)) or ( ((mask & (1 << i))==0) and (i>=n) and ((mask & (1 << city)) != 0) and ( (mask & (1 << cicle[city]))!=0) ))
        {

            //Si se visita un lugar para entregar el producto, el producto tiene 
            //que haber sido recogido antes
            //Si se visita un lugar para recoger un producto, no puede haber sido visitado
            // Si la ciudad i no ha sido visitada, visitarla y actualizar la máscara
            int newCost = cost[curr][i] + totalCost((mask | (1 << i)), i, m, cost, memo, path,cicle);
            if (newCost < ans) {
                ans = newCost;
                nextCity = i;
            }
        }
    }

    // Almacenar el siguiente lugar en la ruta
    path[curr][mask] = nextCity;

    return memo[curr][mask] = ans;
}


pair<int, vector<int>> best_delivery(vector<vector<int>> &cost, vector<int> &pickup_place)
{
    int n = cost.size();
    int m = 2*n-1;
    vector<vector<int>> new_cost(m, vector<int>(m));
    //Duplicar la matriz de entrada para representar las recogidas y entregas de productos
    for(int i = 0; i < m; i++)
    {
        for (size_t j = 0; j < m; j++)
        {
            int r = i<n ? i : i%n+1;
            int c = j<n ? j : j%n+1;
            new_cost[i][j]=cost[r][c];
        }
        
    }

    vector<vector<int>> memo(m, vector<int>(1 << m, -1));
    vector<vector<int>> path(m, vector<int>(1 << m, -1));

    // Comenzar desde el origen, y solo el lugar 0 está visitado inicialmente (máscara = 1)
    int minCost = totalCost(1, 0, m, new_cost, memo, path,pickup_place);

    // Reconstruir la ruta
    vector<int> route;
    int mask = 1;
    int currCity = 0;
    route.push_back(currCity);

    while(true)
    {
       int nextCity = path[currCity][mask];
       route.push_back(nextCity);
       mask |= (1 << nextCity);
       if(nextCity==0)
       {
        break;
       }
        currCity = nextCity; 

    }
    return {minCost, route};

}



int main() {

    vector<vector<int>> cost = {{0,  3,  4, 2, 7},
                                {3,  0,  4,  6, 3},
                                {4,  4,  0,  5, 8},
                                {2, 6,  5,  0, 6},
                                {7,  3,  8,  6, 0}};

    vector<int> pickup_place = {-1,2,4,1,3};

    // vector<vector<int>> cost = {{0,  3,  4,  8,  7},
    //                             {3,  0,  1,  5,  6},
    //                             {4,  1,  0,  7,  4},
    //                             {8,  5,  7,  0,  2},
    //                             {7,  6,  4,  2,  0}};
    // vector<int> pickup_place = {-1,3, 0, 1, 2};                           
    auto result = best_delivery(cost,pickup_place);
    int res = result.first;
    vector<int> route = result.second;

    cout << "Costo mínimo: " << res << endl;
    cout << "Ruta: ";
    for (int city : route) {
        int r = city<cost.size() ? city : city%cost.size()+1;
        cout << r << " ";
    }
    cout << endl;

    return 0;
}

