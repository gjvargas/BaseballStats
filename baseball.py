import argparse
import pickle


class Heap:

    def __init__(self, sorting_key):
        """Initializes a new instance of a heap.

        Args:
            sorting_key: Specifies the attribute of the object inserted
            into the heap, on the basis of which the heap was created.
        """
        self.heap = list()
        self.mapping = dict()
        self.sorting_key = sorting_key

    ##########################################################################
    # STANDARD HEAP OPERATIONS
    ##########################################################################

    def heapify_up(self, child):
        """Standard heapify operation, as described in CLRS.
        Works by swapping the element originially at index child in the heap
        with its parent until the heap property is satisfied. Modifies the
        appropriate heap attribute

        Args:
            child: Index of the element that violates the heap property

        Returns:
            None
        """
        parent = (child - 1) / 2
        # Swaps the element originally at the index child with its parent
        # until the value of the specifed attribute of the parent is greater
        # than the value of the specified attribute of the element itself
        while (getattr(self.heap[parent], self.sorting_key) <
               getattr(self.heap[child], self.sorting_key)):
            if (parent == -1):
                # This means child was 0, which means we have reached the
                # top of the heap
                return

            # Swap the mappings as well to ensure that future references in
            # the mapping dict refer to the correct position of the object in
            # the heap
            self.mapping[self.heap[parent].player] = child
            self.mapping[self.heap[child].player] = parent

            # Swap the parent and the child
            temp = self.heap[parent]
            self.heap[parent] = self.heap[child]
            self.heap[child] = temp

            # Move the child and parent pointers up the heap
            child = parent
            parent = (child - 1) / 2

    def heapify_down(self, parent):
        """Same as heapify_up, but moves an element down instead of up.

        Args:
            parent: Index of the element that violates the heap property

        Returns:
            None
        """
        left = parent*2+1
        right = parent*2+2
        if(len(self.heap) <= left):
            return
        elif(len(self.heap) <= right):
            child = left
        elif (getattr(self.heap[left], self.sorting_key) > getattr(self.heap[right], self.sorting_key)):
            child = left
        else:
            child = right
        while (getattr(self.heap[parent], self.sorting_key) < getattr(self.heap[child], self.sorting_key)):
            if (child >= len(self.heap)):
                # This means child was 0, which means we have reached the
                # top of the heap
                return

            # Swap the mappings as well to ensure that future references in
            # the mapping dict refer to the correct position of the object in
            # the heap
            self.mapping[self.heap[parent].player] = child
            self.mapping[self.heap[child].player] = parent

            # Swap the parent and the child
            temp = self.heap[parent]
            self.heap[parent] = self.heap[child]
            self.heap[child] = temp

            # Move the child and parent pointers up the heap
            parent = child
            left = parent*2+1
            right = parent*2+2
            if(len(self.heap) <= left):
                break
            elif(len(self.heap) <= right):
                child = left
            elif (getattr(self.heap[left], self.sorting_key) >  getattr(self.heap[right], self.sorting_key)):
                child = left
            else:
                child = right


    def extract_max(self):
        """Returns the maximum element in the specified heap

        Returns:
            An object from the heap with maximum value of self.sorting_key
        """
        if(len(self.heap) < 1):
            return
        #Take the max value
        temp = self.heap[0]
        #swap first and last values in heap
        self.heap[0] = self.heap[len(self.heap) - 1]
        self.heap[len(self.heap) - 1] = temp
        #remove last output/max value from heap
        output = self.heap.pop(len(self.heap) - 1)
        #fix heap to satisfy invariant
        self.heapify_down(0)
        return output

    def insert(self, element):
        """Inserts element into the specified heap. Modifies the internal heap
        data structure

        Args:
            element: PlayerRecord object that needs to be inserted into the
            heap

        Returns:
            None
        """

        # Append the new element to the end of the heap, and then
        # move the element up the heap as necessary
        self.heap.append(element)
        child = len(self.heap) - 1
        self.mapping[element.player] = child

        self.heapify_up(child)

    def get_index(self, element):
        """Returns the index of the provided element in the heap

        Args:
            element: The element whose index needs to be returned

        Returns:
            Index of the element in the heap if the element is in the heap
            None, otherwise
        """
        return self.mapping.get(element.player, None)

    def validate_heap(self):
        """Validates that the heap specified by heap_name satisfies the heap
        property at every node

        Returns:
            True if heap property is satisfied at every node of the heap,
            False otherwise
        """
        heap = [getattr(ele, self.sorting_key) for ele in self.heap]
        remaining_elements = [0]
        n = len(heap)
        while (len(remaining_elements) != 0):
            parent = remaining_elements.pop()
            child1 = (2 * parent) + 1
            child2 = (2 * parent) + 2
            if (child1 < n):
                remaining_elements.append(child1)
                if (heap[child1] > heap[parent]):
                    return False
            if (child2 < n):
                remaining_elements.append(child2)
                if (heap[child2] > heap[parent]):
                    return False
        return True


# Statistics for a particular player are encapsulated by a PlayerRecord
class PlayerRecord:

    """Encapsulates statistics of a player

    Attributes:
        player: Name of the player
        ab: Number of at-bats by the player
        hits: Number of 'hits' by the player
        avg: Average number of hits = hits / ab
        rbi: Number of 'runs-batted-in' by the player
    """

    def __init__(self, player, ab, hits, rbi):
        """Initializes a new instance of PlayerRecord, setting the
        various statistic values as provided

        Args:
            player: Name of the player
            ab: Number of at-bats by the player
            hits: Number of hits by the player
            rbi: Number of rbis by the player
        """
        self.player = player

        self.ab = ab
        self.hits = hits
        if ab == 0:
            self.avg = 0.0
        else:
            self.avg = float(hits) / float(ab)
        self.rbi = rbi

    def __repr__(self):
        return '%s--Ab:%d, Hits:%d, Avg:%.3f, Rbi:%d' % (
            self.player, self.ab, self.hits, self.avg, self.rbi)


class Problem:

    """Represents an instance of a problem. Implements operations required in
    the problem statement

    Attributes:
        player_record_mapping: Mapping between player name and PlayerRecord
        object corresponding to the player
    """

    def __init__(self):
        self.player_record_mapping = dict()
        self.abHeap = Heap('ab')
        self.hitsHeap = Heap('hits')
        self.rbiHeap = Heap('rbi')
        self.avgHeap = Heap('avg')

    ###########################################################################
    # Batting operations
    ###########################################################################

    def new_at_bat(self, player, hits, rbi):
        """Represents the new_at_bat operation. Checks if the given player
        has been seen before, if so just updates the corresponding PlayerRecord
        object (and corresponding heaps as well); otherwise creates a new
        object of the PlayerRecord class corresponding to the new player
        and adds this new object to all required heaps

        Args:
            player: Name of the player whose record needs to created / updated
            hits: Number of hits
            rbi: Number of runs-batted-in

        Returns:
            None
        """
        if player in self.player_record_mapping:
            currentRecord = self.player_record_mapping[player]
            currentRecord.ab = currentRecord.ab + 1
            currentRecord.hits = currentRecord.hits + hits
            currentRecord.rbi = currentRecord.rbi + rbi
            currentRecord.avg = float(currentRecord.hits)/float(currentRecord.ab)
            self.player_record_mapping[player] = currentRecord
            self.abHeap.heapify_up(self.abHeap.get_index(currentRecord))
            self.hitsHeap.heapify_up(self.hitsHeap.get_index(currentRecord))
            self.rbiHeap.heapify_up(self.rbiHeap.get_index(currentRecord))
            if(hits == 0):
                self.avgHeap.heapify_down(self.avgHeap.get_index(currentRecord))
            else:
                self.avgHeap.heapify_up(self.avgHeap.get_index(currentRecord))
        else:
            playerRecord = PlayerRecord(player, 1, hits, rbi)
            self.abHeap.insert(playerRecord)
            self.hitsHeap.insert(playerRecord)
            self.rbiHeap.insert(playerRecord)
            self.avgHeap.insert(playerRecord)

            self.player_record_mapping[player] = playerRecord
            

    def current_stats(self, player):
        """Represents the current_stats operation.

        Args:
            player: Name of the player

        Returns:
            PlayerRecord instance that encapsulates statistics of the
            specified player if the player name exists in the database.
            PlayerRecord(None, 1, 0, 0) if the player name does not exist
            in the database.
        """
        if player in self.player_record_mapping:
            return self.player_record_mapping[player]
        else:
            return PlayerRecord(None, 1, 0, 0)

    def current_best(self, stat, k):
        """Represents the current_best operation.

        Args:
            stat: The type of statistic for which we need to return
            the top k players
            k: The number of players to return
        Returns:
            If k <= n, a list of k PlayerRecord objects in decreasing order of
            the given statistic
            If k > n, a list of n PlayerRecord objects in decreasing order of
            the given statistic
        """
        #Use the appropriate heap
        theHeap = None;
        if (stat == 'ab'):
            theHeap = self.abHeap
        elif(stat == 'hits'):
            theHeap = self.hitsHeap
        elif(stat == 'rbi'):
            theHeap = self.rbiHeap
        elif(stat == 'avg'):
            theHeap = self.avgHeap
        else:
            print 'not valid'
            return
        output = []
        size = min(k, len(theHeap.heap))
        #find k max statistics
        for i in range(size):
            output.append(theHeap.extract_max())
        #reinsert k max statistics
        for i in output:
            theHeap.insert(i)
        return output


def run(filename, debug=False):
    """Runs the code specified in the Program class against the provided
    test driver file.

    Args:
        filename: File path of the test driver file
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
        return run_from_list(lines, debug)
    return None


def run_from_list(line_list, debug=False):
    """Runs the code specified in the Program class against the provided
    line_list

    Args:
        line_list: List of input lines

    Returns:
        List of results
    """
    problem = Problem()
    results = list()
    for line in line_list:
        line = line.strip()
        tokens = line.split('\t')
        operation_type = tokens[0]
        # Following operations allowed:
        # 1. n -- new_at_bat(player, hits, rbi)
        # 2. cs -- current_stats(player)
        # 3. cb -- current_best(heap_name, k)
        if (operation_type == 'n'):
            player = tokens[1]
            hits = int(tokens[2])
            rbi = int(tokens[3])
            problem.new_at_bat(player, hits, rbi)
        elif (operation_type == 'cs'):
            player = tokens[1]
            cs = problem.current_stats(player)
            results.append(
                ('cs', (cs.player, cs. ab, cs.hits, cs.avg, cs.rbi)))
            if debug:
                print cs
        elif (operation_type == 'cb'):
            heap_name = tokens[1]
            k = int(tokens[2])
            cb = problem.current_best(heap_name, k)
            transformed_cb = [
                (stat.player, stat.ab, stat.hits, stat.avg, stat.rbi)
                for stat in cb]
            results.append((('cb', heap_name), transformed_cb))
            if debug:
                print cb
    return results


def process_results(results):
    MAPPING = {'player': 0, 'ab': 1, 'hits': 2, 'avg': 3, 'rbi': 4}
    processed_results = list()
    for result in results:
        (result_type, val) = result
        if result_type == 'cs':
            processed_results.append(val)
        else:
            (_, heap_name) = result_type
            processed_list = [element[MAPPING[heap_name]] for element in val]
            processed_results.append(processed_list)
    return processed_results


if __name__ == '__main__':
    import cProfile
    parser = argparse.ArgumentParser(description='Program arguments')
    parser.add_argument('--c', action='store_true')
    parser.add_argument('input_file')
    args = parser.parse_args()
    input_lines, gold_processed_results, _ = pickle.load(open(args.input_file))
    if args.c:
        results = run_from_list(input_lines)
        processed_results = process_results(results)
        if processed_results != gold_processed_results:
            print "TEST FAILED"
        else:
            print "TEST PASSED"
    else:
        cProfile.run("run_from_list(input_lines)")
