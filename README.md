# **Problema del Intercambio de Medicamentos en Cuba**

## Autores:
- Paula Silva Lara C412
- Ricardo Cápiro Colomar C412
- Edián Broche Castro C412

## **Descripción del problema**  

En el actual contexto de crisis en Cuba, el acceso a medicamentos esenciales se ha visto gravemente afectado por múltiples factores, entre ellos: la escasez de suministros médicos debido a restricciones económicas, dificultades logísticas y problemas en la producción nacional. En este panorama, muchos cubanos recurren a formas informales de intercambio de medicamentos como una alternativa para cubrir sus necesidades de salud.  

El mercado de intercambio de medicamentos en Cuba no sigue los principios tradicionales de un mercado regulado. Más bien, opera como una red comunitaria en la que los ciudadanos intercambian los medicamentos que poseen, aunque no los necesiten, por aquellos que sí son fundamentales para ellos o sus familiares. Este fenómeno ha emergido como un mecanismo de supervivencia para enfrentar la falta de acceso regular a medicamentos en farmacias y hospitales.  

## **Problemas Claves en el Contexto Cubano**  
1. **Escasez Generalizada**  
   - Los medicamentos esenciales, como antihipertensivos, antibióticos, antidiabéticos e incluso analgésicos básicos, son difíciles de encontrar en farmacias oficiales.  
   - Esto obliga a las personas a buscar alternativas en redes informales.  

2. **Dependencia de Redes Sociales y Conexiones Informales**  
   - Los intercambios suelen organizarse a través de contactos personales, grupos comunitarios, e incluso plataformas digitales como WhatsApp y Telegram.  
   - Estas redes no siempre son eficientes, lo que genera desigualdad en el acceso.  

3. **Desperdicio y Pérdida de Medicamentos**  
   - Medicamentos que podrían ser útiles para otros permanecen almacenados en manos de quienes no los necesitan, mientras que otros carecen de acceso a ellos.  

4. **Desafíos Éticos y Logísticos**  
   - La ausencia de regulación puede dar lugar a intercambios injustos o aprovechamiento de la necesidad ajena.  
   - Algunos medicamentos requieren condiciones de almacenamiento específicas, lo que puede comprometer su eficacia durante los intercambios.  


## **Formulación**  

1. **Conjunto de Agentes y Medicamentos**  
   - Sea $ A = \{a_1, a_2, \dots, a_n\} $ el conjunto de agentes.  
   - Cada agente $ a_i $ tiene un medicamento $ m_i $ que desea intercambiar y busca un medicamento $ m_i^d $ que necesita.  


2. **Graficación del Problema**  
   - Representamos el problema como un grafo dirigido $ G = (V, E) $, donde:  
     - $ V = A $ es el conjunto de agentes (nodos).  
     - $ E \subseteq V \times V $ es el conjunto de aristas, donde existe una arista $ (a_i, a_j) $ si el medicamento $ m_i $ ofrecido por $ a_i $ coincide con el medicamento deseado $ m_j^d $ de $ a_j $.  
  

3. **Restricciones de los Ciclos**  

   - La longitud máxima de un ciclo es $ L_{\text{max}} $, una constante positiva. 
   - Todos los medicamentos en un ciclo deben intercambiarse simultáneamente. 

## **Naturaleza del Problema**  
Este problema no es polinomial porque implica buscar la mejor manera de emparejar a los participantes en ciclos de intercambio, teniendo en cuenta la longitud máxima de los ciclos. La dificultad radica en que, para encontrar la solución óptima, se deben explorar todas las posibles combinaciones de ciclos en el grafo, y el número de estas combinaciones crece exponencialmente con el número de participantes.  

Además, cada ciclo tiene que cumplir ciertas condiciones específicas, como que todos los intercambios del ciclo sean compatibles y puedan realizarse simultáneamente. Estas restricciones hacen que no baste con usar métodos simples como los que funcionan en problemas polinomiales, porque no hay un camino directo para resolverlo rápidamente conforme el problema crece.  

Por eso, modelarlo de forma simple no es práctico, y se necesitan técnicas avanzadas como metaheurísticas (que buscan buenas soluciones sin garantizar que sean óptimas) o algoritmos especializados que puedan manejar la complejidad y encontrar soluciones razonables en un tiempo aceptable. Estas aproximaciones sacrifican algo de perfección a cambio de ser mucho más rápidas y manejables en la práctica.  

