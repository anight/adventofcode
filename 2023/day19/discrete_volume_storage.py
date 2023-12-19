
class DiscreteVolumeStorage(object):
	def __init__(self):
		self.storage = []

	def set(self, new_aabb, v):
		i = 0
		while i < len(self.storage):
			aabb = list(self.storage[i])
			skip = False
			cuts = []
			for j, ((start, stop), (new_start, new_stop)) in enumerate(zip(aabb, new_aabb)):
				if stop <= new_start or new_stop <= start:
					skip = True
				elif stop > new_stop or start < new_start:
					if start < new_start < stop:
						cuts.append(aabb[:j] + [ (start, new_start) ] + aabb[j+1:])
					if start < new_stop < stop:
						cuts.append(aabb[:j] + [ (new_stop, stop) ] + aabb[j+1:])
					aabb[j] = ( max(start, new_start), min(stop, new_stop) )
			if skip:
				i += 1
				continue

			if len(cuts) > 0:
				self.storage += cuts

			self.storage.pop(i)

		if v:
			self.storage.append(new_aabb)

	def volume(self):
		total = 0
		for aabb in self.storage:
			volume = 1
			for start, stop in aabb:
				volume *= (stop - start)
			total += volume
		return total

	def __setitem__(self, k, v):
		aabb = []
		for s in k:
			assert type(s) is slice
			assert s.stop > s.start
			assert s.step is None or s.step == 1
			aabb.append( (s.start, s.stop) )
		self.set(aabb, v)

