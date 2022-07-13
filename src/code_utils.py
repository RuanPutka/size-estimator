import numpy as np
from src.graph_utils.utils import normalize_dag_edges
from src.directed_acyclic_graph.my_ordered_dict import MyOrderedDict
from src.directed_acyclic_graph.directed_acyclic_graph import DirectedAcyclicGraph as DAG


def _get_number_of_non_null_intersections(vec1, vec2):
    return sum(np.logical_and(~np.isnan(vec1), ~np.isnan(vec2)))


def get_number_of_intersections(arr, keep_zeros=False):
    """
    Parameters
    ----------
    arr: (m(products) x n(stores)) np.array.
         Values are the sell-out information of the m products in the n stores.

    keep_zeros: Boolean (False by default).
        Store cases with zero intersection or not.

    Returns
    -------
    Python dictionary containing tuples as keys corresponding to the arrays row numbers
    that are beign compared, and values equal to the number of non null values that
    are positional matched column-wise.


    """
    results = MyOrderedDict()
    for i, i_values in enumerate(arr):
        for j, j_values in enumerate(arr):
            if j != i:
                intersecstion_count = _get_number_of_non_null_intersections(i_values, j_values)
                if (not keep_zeros) and (intersecstion_count > 0):
                    results[(i, j)] = intersecstion_count
                elif keep_zeros:
                    results[(i, j)] = intersecstion_count

    return results


def calculate_rows_ratio(arr, iloc_pair):
    return np.nanmean(arr[iloc_pair[0], :]/ arr[iloc_pair[1], :])


def _get_intersected_columns_index(vec1, vec2):
    vec1_not_null = ~np.isnan(vec1)
    vec2_not_null = ~np.isnan(vec2)
    true_columns_indices = []
    number_of_columns = len(vec1)
    for column_index in range(number_of_columns):
        if vec1_not_null[column_index] == True and vec2_not_null[column_index] == True:
            true_columns_indices.append(column_index)
                
    return true_columns_indices


def _get_rowwise_dispersion_index(vec1, vec2):
    residuals = vec1 / vec2 
    dispersion_index = np.std(residuals) / np.mean(residuals)
    
    return dispersion_index


def get_dispersion_index(arr, min_intersections=1):
    results = MyOrderedDict()
    already_iterated = []
    for i, i_values in enumerate(arr):
        already_iterated.append(i)
        for j, j_values in enumerate(arr):
            if j != i:
                intersecstion_count = _get_number_of_non_null_intersections(
                    i_values,
                    j_values
                    )
                if (intersecstion_count >= min_intersections):
                    intersected_columns = _get_intersected_columns_index(
                        i_values,
                        j_values
                        )
                    results[(i, j)] =  _get_rowwise_dispersion_index(
                        i_values[intersected_columns],
                        j_values[intersected_columns]
                        )
    return results


def get_number_of_intersections_divided_by_larger_set_size(arr, keep_zeros=False):
    """
    Parameters
    ----------
    arr: (m(products) x n(stores)) np.array.
         Values are the sell-out information of the m products in the n stores.

    keep_zeros: Boolean (False by default).
        Store cases with zero intersection or not.

    Returns
    -------
    Python dictionary containing tuples as keys corresponding to the arrays row numbers
    that are beign compared, and values equal to the number of non null values that
    are positional matched column-wise.


    """
    results = MyOrderedDict()
    for i, i_values in enumerate(arr):
        for j, j_values in enumerate(arr):
            if j != i:
                intersecstion_count = _get_number_of_non_null_intersections(i_values, j_values)
                highest_set_size = max(sum(~np.isnan(i_values)), sum(~np.isnan(j_values)))
                if (not keep_zeros) and (intersecstion_count > 0):
                    results[(i, j)] = intersecstion_count / highest_set_size
                elif keep_zeros:
                    results[(i, j)] = intersecstion_count / highest_set_size

    return results
    
    
    

def swap(tuple):
    a = tuple[0]
    b = tuple[1]

    return (b, a)